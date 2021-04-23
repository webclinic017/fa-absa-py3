"""The new aggregation/aggregation module.

For documentation of the whole process please see confluence:
ABCap Front Arena -> Projects -> New aggregation process

Uses ael, because acm thinks commited archived objects are deleted, which
doesn't allow for a clean rollback.

C1024176    Jan Sinkora         Initial deployment.
C1079567    Jan Sinkora         Updated of cash-posting trades, refactored trade
                                aggregation, more strict cash posting trades
                                identification, refactored FParametersDict into
                                at_collections.
"""
import ael, acm
from collections import defaultdict
from datetime import datetime
import os

from aggregation_constants import LOCKED_TRADE_TEXT
from at_collections import FParametersDict, Enum
from at_functools import cache_first_result
from at_logging import getLogger

LOGGER = getLogger()
AGGREGATION_USER = 'FMAINTENANCE'
TRANSACTION_CHUNK_SIZE = 15000

def dict_list_lengths(data):
    """Map lists in the dict values to their lengths."""
    return dict((k, len(v)) for k, v in data.iteritems())

def transactioned(log=LOGGER):
    """A method decorator that envelops the method into a transaction.

    If the transaction fails, this re-raises the exception that caused it.

    """
    def decorate(method):
        def transactioned_method(*args, **kwargs):
            ael.begin_transaction()
            try:
                method(*args, **kwargs)
                ael.commit_transaction()
            except:
                # This has to happen regardless of what was raised.
                ael.abort_transaction()
                if log:
                    log.exception("Transaction aborted.")
                raise

        return transactioned_method
    return decorate

def states_required(*states):
    """A method decorator that checks if the batch is in one of the states."""

    def decorate(method):
        def checked_method(self, *args, **kwargs):
            if self.config['aggregation_state'] not in states:
                msg = "States '{0}' are required for this action, batch is in '{1}'"
                raise Aggregation.StateError(msg.format(states,
                    self.config['aggregation_state']))

            return method(self, *args, **kwargs)
        return checked_method
    return decorate

def initialization_required(method):
    def checked_method(self, *args, **kwargs):
        """Check if this batch is initialized."""
        if not self._initialized:
            raise Aggregation.GeneralError("The instance was not initialized with input data.")

        return method(self, *args, **kwargs)
    return checked_method

def archived_mode_required(method):
    """Check if the script is running in archived mode."""

    def checked_method(*args, **kwargs):
        if acm.ArchivedMode() == 0:
            raise Aggregation.GeneralError("Running de-aggregation in non-archived mode.")

        return method(*args, **kwargs)
    return checked_method

def agg_user_required(method):
    """Check if the script is run under the correct user."""

    def checked_method(*args, **kwargs):
        if acm.User().Name() != AGGREGATION_USER:
            raise Aggregation.GeneralError("Attempting to run aggregation by user other than {0}.".format(AGGREGATION_USER))

        return method(*args, **kwargs)
    return checked_method


class AggregationConfig(FParametersDict):
    """
    This is an adjustment of FParametersDict for convenient aggregation configuration.

    """

    CONFIG_NAME_TPL = 'Aggregation_{0}'

    @staticmethod
    @cache_first_result
    def _ext_module():
        return FParametersDict._ext_context().GetModule(AGGREGATION_USER)

    @agg_user_required
    def __init__(self, name, create=False):
        """Initialize with the given name and creation flag.

        Raises ValueError if the config doesn't exist.

        """
        FParametersDict.__init__(self, name, AGGREGATION_USER, create)

    def _default_values(self):
        """The default values - initial status and date."""
        return {'aggregation_state': Aggregation.STATES.SETUP}

    @classmethod
    def _name_for_date(cls, date):
        """Return the name of the FParameters extension for the given date.

        Raises ValueError if the format is wrong.

        """
        # Check the date format
        datetime.strptime(date, '%Y-%m-%d')

        return cls.CONFIG_NAME_TPL.format(date)

    @classmethod
    def from_date(cls, date):
        """Return the config for the given date.

        Raises ValueError if the config doesn't exist.

        """
        return cls(cls._name_for_date(date))

    @classmethod
    def create(cls, date):
        """Create a new config with the given date.

        Use this for proper config creation.

        """
        config = cls(cls._name_for_date(date), True)
        config['date'] = date
        return config

    @classmethod
    def select_all(cls, aggregation_type=None):
        """Get all saved instances of the config class."""

        param_names = FParametersDict._all_dict_names(cls._ext_module())
        params = list(map(cls, param_names))

        # For the dict to be an aggregation config, it has to have the aggregation_state key
        filtered = filter(lambda p: 'aggregation_state' in p, params)
        if aggregation_type:
            filtered = filter(lambda p: p['type'] == aggregation_type, filtered)

        return filtered


class AggregationConfigMO(AggregationConfig):
    CONFIG_NAME_TPL = 'Aggregation_MO_{0}'

    @staticmethod
    def _load_aggregate_trdnbrs(encoded_value):
        """Callback for the aggregate_trdnbrs key loading."""
        return list(map(int, encoded_value.split(',')))

    @staticmethod
    def _save_aggregate_trdnbrs(decoded_values):
        """Callback for the aggregate_trdnbrs key loading."""
        return ",".join(map(str, decoded_values))


class Aggregation(object):
    """Abstract class subclasses of which control the different aggregation batches.

    Control of the batches is then done through this class' interface.

    """

    class GeneralError(RuntimeError):
        """A general error during aggregation."""

    class CheckError(GeneralError):
        """This is raised when entities fail pre-archiving checks."""

    class StateError(GeneralError):
        """An error with the state machine."""

    AGGREGATION_TYPE = None
    CONFIG_CLASS = AggregationConfig

    # Various states of the batch.
    # SETUP         initial phase, without input data
    # PREPARED      input data provided, ready to run (also after a successful rollback)
    # RUNNING       temporary state during aggregation run
    # FINALIZING    temporary state during finalization
    # FINISHED      final state (success)
    # ROLLING_BACK  temporary state during rollback in response to a failure during RUNNING
    # BROKEN        final state (failure during rollback)
    # RESETTING     temporary state during complete reset (from FINISHED or BROKEN)
    # DELETED       temporary state, the batch config is removed from storage
    STATES = Enum(['SETUP',
                   'PREPARED',
                   'RUNNING',
                   'FINALIZING',
                   'FINISHED',
                   'ROLLING_BACK',
                   'BROKEN',
                   'RESETTING',
                   'DELETED'])

    # Allowed transitions.
    TRANSITIONS = {STATES.SETUP: [STATES.PREPARED, STATES.DELETED],
                   STATES.PREPARED: [STATES.RUNNING, STATES.SETUP],
                   STATES.RUNNING: [STATES.FINALIZING, STATES.ROLLING_BACK],
                   STATES.FINALIZING: [STATES.FINISHED, STATES.ROLLING_BACK, STATES.BROKEN],
                   STATES.ROLLING_BACK: [STATES.PREPARED, STATES.BROKEN],
                   STATES.FINISHED: [STATES.RESETTING],
                   STATES.BROKEN: [STATES.RESETTING],
                   STATES.RESETTING: [STATES.PREPARED, STATES.BROKEN]}

    def possible_transitions(self):
        """Return all possible transitions for this batch."""
        return self.TRANSITIONS.get(self.config['aggregation_state'], [])

    @classmethod
    def add_ael_variables(cls, ael_variables):
        """Adds aggregation-type-specific ael variables to the parameter."""

    def set_ael_variable_values(self, ael_variables):
        """Sets the optional parameters' values in the ael_variables."""

    def get_values_from_ael_variables(self, ael_variables):
        """Gets values of parameters from the associated ael variables."""

    @classmethod
    def _type_prefix(cls, input_str):
        return '_'.join((cls.AGGREGATION_TYPE, input_str))

    @agg_user_required
    def __init__(self, config, log=LOGGER):
        """Initialize the aggregation batch.

        config is a config object. Use from_name to initialize by object name.

        """
        self.config = config
        self._initialized = False
        self._log = log
        self.errors = []

    def setup_from_ael_params(self, params):
        """Setup the batch from the provided ael variable values."""
        self.setup(*self.get_values_from_ael_params(params))

    def setup(self):
        """Setup the batch with the required parameters."""
        self._initialized = True

    def name(self):
        """Return the name of this batch."""
        return str(self.config.name)

    @initialization_required
    @states_required(STATES.SETUP)
    def prepare(self):
        """Prepare this aggregation batch.

        Calls self._prepare() which should be overriden in subclasses if needed.

        """

        self._log.info("Preparing.")
        self._safe_prepare()
        self._log.info("Preparing complete.")

        self._set_state(self.STATES.PREPARED)


    @transactioned(LOGGER)
    def _safe_prepare(self):
        """Transactioned wrapper of the worker method _prepare()."""
        self._prepare()


    def _prepare(self):
        """Worker called by the prepare() method.

        Override in subclasses if needed.

        """

    @initialization_required
    @states_required(STATES.PREPARED)
    def cancel(self):
        """Revert from PREPARED to SETUP.

        This should cancel what prepare() does.

        """

        self._cancel()
        self._set_state(self.STATES.SETUP)

    def _cancel(self):
        """Worker called by the cancel() method.

        Override in subclasses if needed.

        """

    @archived_mode_required
    @states_required(STATES.FINISHED, STATES.BROKEN)
    def reset(self):
        """Revert from FINISHED or BROKEN.

        This should undo whatever run() and finalize() did.

        """

        self._log.info("Resetting the batch - unarchiving entities.")

        self._set_state(self.STATES.RESETTING)
        try:
            self._reset()
            self._set_state(self.STATES.PREPARED)
        except:
            self._log.exception("Resetting failed.")
            self._set_state(self.STATES.BROKEN)
            raise

    def _reset(self):
        """Called by the reset() method.

        Override in subclasses.

        """

    @initialization_required
    @archived_mode_required
    @states_required(STATES.PREPARED)
    def run(self):
        """The main archiving run.

        This checks initialization and inputs before running the achiving.
        If an exception is raised during run, rollback is initiated.

        Possible results: FINISHED or BROKEN.

        """
        # Needs to run in archived mode.
        # Otherwise takes very long due to unsubscribing of archived trades.

        if self.check_inputs():
            self._log.info("Pre-check of inputs ok.")
            self._set_state(self.STATES.RUNNING)
            self._log.info("Archiving.")

            try:
                self._archive()
                self._set_state(self.STATES.FINALIZING)
                self.finalize()
            except:
                self._log.error("Archiving error, initiating rollback.")
                self.rollback()
                raise
            else:
                self.config['date'] = acm.Time.DateToday()
        else:
            for e in self.errors:
                self._log.error(e)
            raise Aggregation.CheckError("There were errors in the trade pre-check phase.")

    @initialization_required
    def check_inputs(self):
        """Wrapper for the _check_inputs custom method."""
        return self._check_inputs()

    def _check_inputs(self):
        """Check if all inputs are ok.

        This should return true or false.
        Any errors should be added to self.errors.

        """
        raise NotImplementedError

    def _archive(self):
        """Worker that should do the archiving."""
        raise NotImplementedError

    @initialization_required
    def rollback(self):
        """Rollback used in case of a running failure.

        This calls the _rollback worker method for the rollback logic itself.

        """

        # Not checking state, because rollback must happen either way.
        self._set_state(self.STATES.ROLLING_BACK)

        self._log.info("Rolling back.")
        try:
            self._rollback()
            self._set_state(self.STATES.PREPARED)
            self._log.info("Rollback complete.")
        except:
            self._set_state(self.STATES.BROKEN)
            self._log.error("Rollback failed.")
            raise

    def _rollback(self):
        """Worker for rollback."""
        raise NotImplementedError

    @states_required(STATES.SETUP)
    def delete(self):
        """Delete this aggregation batch."""
        # Call the deletion worker method.
        self._delete()

        # Delete the batch config.
        self.config.delete()

    def _delete(self):
        """Called when deleting the batch via the delete() method.

        Override in subclasses for cleanup (temporary files etc.)

        """

    @states_required(STATES.FINALIZING)
    def finalize(self):
        """Finalize the aggregation process."""
        self._log.info("Finalizing.")
        self._safe_finalize()
        self._set_state(self.STATES.FINISHED)


    @transactioned(LOGGER)
    def _safe_finalize(self):
        """Transactioned wrapper of the worker method _finalize()."""
        self._finalize()


    def _finalize(self):
        """Worker called by the finalize() method.

        Override in subclasses if needed.

        """


    @classmethod
    def create(cls, date, description='', log=LOGGER):
        """Create the aggregation config and return the aggregation batch instance."""
        config = cls.CONFIG_CLASS.create(date)
        config.update({'date': date,
                       'description': description,
                       'type': cls.AGGREGATION_TYPE})
        return cls(config)


    @classmethod
    def select_all(cls, log=LOGGER):
        """Get all saved instances of archiving batches."""
        return [cls(config, log) for config in cls.CONFIG_CLASS.select_all(
            cls.AGGREGATION_TYPE)]


    @classmethod
    def from_name(cls, name, log=LOGGER):
        """Gets an instance with the given name (None if not existing)."""
        config = cls.CONFIG_CLASS(name)
        return cls(config, log)


    @classmethod
    def from_date(cls, date, log=LOGGER):
        """Gets an instance with the given date (None if not existing)."""
        try:
            config = cls.CONFIG_CLASS.from_date(date)
        except cls.CONFIG_CLASS.DoesNotExist:
            # config doesn't exist
            return None
        return cls(config, log)


    def _set_state(self, state):
        """Transits into the given state if it's allowed by the transition rules."""
        if not state in self.STATES:
            raise ValueError("State '{0}' is not supported.".format(state))

        if state not in self.possible_transitions():
            self._log.warning("Wrong transition: '{0}' -> '{1}'.".format(self.config['aggregation_state'], state))

        self.config['aggregation_state'] = state


class TradeAggregation(Aggregation):
    """Trade-specific aggregation class.

    This handles the archiving of trades and their payments, settlements and addinfos.
    This is an abstract class for any Trade related archiving, see TradeAggregationMO
    for an example of usage.

    """

    AGGREGATION_LEVEL = 2
    CONFIG_CLASS = AggregationConfigMO

    LINKED_OBJECTS = ('payments',
                      'settlements',
                      'additional_infos',
                      'trade_account_links',
                      'confirmations')

    @classmethod
    def get_all_linked(cls, trade):
        """Get a dict with keys = LINKED_OBJECTS, values = lists of objects."""
        return dict([(method, getattr(trade, method)()) for method in cls.LINKED_OBJECTS])


    @classmethod
    def _chunkify(cls, trades):
        """Split the trades into chunks that will not commit more than
        TRANSACTION_CHUNK_SIZE entities.

        """
        trade_counts = [(t, 1 + sum(map(len, cls.get_all_linked(t).values())))
                        for t in trades]

        current_chunk = []
        trade_chunks = [current_chunk]
        count = 0
        for trade, trade_count in trade_counts:
            if count + trade_count > TRANSACTION_CHUNK_SIZE:
                # trade goes to next chunk
                current_chunk = []
                trade_chunks.append(current_chunk)
                count = trade_count
            else:
                # trade goes to current chunk
                count += trade_count
            current_chunk.append(trade)

        return trade_chunks


    def _archive(self):
        """Archive the chunks."""
        self._log.info("Chunks: {0}.".format(len(self._archivists)))

        try:
            for last_chunk, archivist in enumerate(self._archivists):
                last_chunk += 1
                # chunk now contains all trades that will be archived in one transaction
                self._log.info("Chunk {0}: {1} trades.".format(last_chunk, archivist.count()))
                archivist.run()

            self._log.info("Archiving complete.")
        except:
            # This triggers rollback, has to happen.
            self._log.error("Chunk {0} failed.".format(last_chunk))
            raise

        self._log.info("Collecting statistics.")
        counts = self.summary()

        stats = {}
        for entity_type, count in counts.iteritems():
            self._log.info("Entity type: {0}, count: {1}.".format(entity_type, count))
            stats['stats_{0}_count'.format(entity_type)] = count

        self.config.update(stats)

        self._log.info("Statistics saved.")

    def _rollback(self):
        """Rollback all the chunks."""
        try:
            for last_chunk, archivist in enumerate(self._archivists):
                last_chunk += 1
                if archivist.finished:
                    self._log.info("Chunk {0}: rolling back.".format(last_chunk))
                    archivist.rollback()
        except:
            self._log.exception("Chunk {0} failed to roll back.".format(last_chunk))
            raise

    def summary(self):
        """Get summary - counts of archived entities."""
        archivist_summaries = [a.summary() for a in self._archivists]
        counts = defaultdict(int)
        for summary in archivist_summaries:
            for entity_type, count in summary.iteritems():
                counts[entity_type] += count

        return counts

    def __repr__(self):
        """Return the name of the batch."""
        return self.name()

class TradeAggregationMO(TradeAggregation):
    """Aggregation used in the current process with MO choosing the trades.

    The input is one file with trade numbers of trades to be archived, each
    mapped to one cash-posting trade. The format is two columns per line,
    separated by a single tab, second number is a cash-posting trade's number.

    """

    AGGREGATION_TYPE = 'trade_mo'

    @classmethod
    def add_ael_variables(cls, ael_variables):
        ael_variables.add(cls._type_prefix('input_folder'),
                          label='Input folder_MO Trades')
        ael_variables.add(cls._type_prefix('mapping_file'),
                          label='Trade mapping file_MO Trades',
                          alt='File with mapping of trades to the cash posting trades')

    def set_ael_variable_values(self, ael_variables):
        ael_variables.get(self._type_prefix('input_folder')).value = self.config['input_folder']
        ael_variables.get(self._type_prefix('mapping_file')).value = self.config['mapping_file']

    def get_values_from_ael_params(self, params):
        return [params[self._type_prefix(param)] for param in ('input_folder', 'mapping_file')]

    def setup(self, input_folder, mapping_file_name):
        """Sets the entities of the aggregations (i.e. trades).

        This must be called before any operations can be performed on the object.

        """
        trade_mapping = self.parse_file(input_folder, mapping_file_name)
        entities = [ael.Trade[t] for t in trade_mapping.keys()]
        self._entities = entities
        self._agg_trdnbrs = set(trade_mapping.values())
        self._agg_trades = [ael.Trade[t] for t in self._agg_trdnbrs]
        self._mapping = trade_mapping
        self._trade_chunks = self._chunkify(entities)
        self._archivists = [TradeArchivistMO(chunk,
            self._mapping, self._log) for chunk in self._trade_chunks]
        self.config['input_folder'] = input_folder
        self.config['mapping_file'] = mapping_file_name
        self.config['aggregate_trdnbrs'] = self._agg_trdnbrs

        self._initialized = True

    def parse_file(self, input_folder, mapping_file, log=LOGGER):
        """Parse the input files.

        Returns tuple (aggregates, mapping).

        """
        mapping_file_full = os.path.join(input_folder, mapping_file)

        try:
            header_check = True
            trade_mapping = {}

            for line in open(mapping_file_full, 'r'):
                if line:
                    values = [nbr.strip() for nbr in line.split(',')]
                    try:
                        values = list(map(int, values))
                    except:
                        # If this is header, just go on.
                        if header_check:
                            header_check = False
                            continue
                        # Otherwise re-raise - wrong format.
                        raise

                    trade_mapping[values[0]] = values[1]

        except Exception as e:
            raise Aggregation.CheckError("Wrong mapping file: {0}.".format(e))

        return trade_mapping


    def _check_inputs(self):
        """Check if all the entities are configured properly for archiving."""
        self.errors = []

        for trdnbr in self._agg_trdnbrs:
            t = ael.Trade[trdnbr]
            if not t:
                self.errors.append("Cash posting trade {0} does not exist".format(trdnbr))
            else:
                if t.aggregate_trdnbr:
                    self.errors.append("Cash posting trade {0} is already set as aggregate".format(t.trdnbr))
                if t.archive_status != 0:
                    self.errors.append("Cash posting trade {0} is archived".format(t.trdnbr))

        for trdnbr, agg_trdnbr in self._mapping.iteritems():
            t = ael.Trade[trdnbr]
            if not t:
                self.errors.append("Trade {0} does not exist".format(trdnbr))
            else:
                if not agg_trdnbr in self._agg_trdnbrs:
                    self.errors.append("Trade {0} mapped to {1}, which is not in the aggregates list".format(t.trdnbr, agg_trdnbr))

        return not self.errors


    def _prepare(self):
        """Prepare the cash-posting trades."""
        owner = ael.User[AGGREGATION_USER]

        for t in self._agg_trades:
            t = t.clone()
            t.owner_usrnbr = owner
            t.type = 'Cash Posting'
            t.text1 = LOCKED_TRADE_TEXT
            t.commit()


    def _cancel(self):
        """Return the cash-posting trades to the normal state."""
        for t in self._agg_trades:
            t = t.clone()
            t.type = 'Normal'
            t.text1 = ''
            t.commit()


    def _load_entities_from_config(self):
        """Load the aggregate trades from config-stored trade numbers.

        This sets up the batch for un-archiving.

        """
        self._agg_trdnbrs = self.config['aggregate_trdnbrs']
        self._agg_trades = [ael.Trade[t] for t in self._agg_trdnbrs]
        self._entities = []
        self._mapping = {}

        for agg_t in self._agg_trades:
            archived_trades = ael.Trade.select('aggregate_trdnbr = {0}'.format(agg_t.trdnbr))
            for t in archived_trades:
                self._mapping[t.trdnbr] = agg_t.trdnbr
            self._entities.extend(archived_trades)

        self._trade_chunks = self._chunkify(self._entities)
        self._archivists = [TradeArchivistMO(chunk,
            self._mapping, self._log) for chunk in self._trade_chunks]
        self._initialized = True


    def _reset(self):
        """Reset all the trades to non-archived."""

        # Load everything from the aggregates trades.
        self._load_entities_from_config()

        # Reset the cash-posting trades' statuses.
        for t in self._agg_trades:
            if t.status != 'Simulated':
                t = t.clone()
                t.status = 'Simulated'
                t.aggregate = 0
                t.commit()

        self._log.info("Unarchiving {0} chunks.".format(len(self._archivists)))
        # Revert the archived trades.
        for i, archivist in enumerate(self._archivists):
            self._log.info("Unarchiving chunk {0}.".format(i + 1))
            archivist.reset()


    def _finalize(self):
        """Finalize - mark cash-posting trades as BO Confirmed."""
        for t in self._agg_trades:
            t = t.clone()
            t.status = 'BO-BO Confirmed'
            t.text1 = ''
            t.aggregate = self.AGGREGATION_LEVEL
            t.commit()


class Archivist(object):
    """The abstract archivist class, handles archiving of a batch of entities.

    Data modifying worker methods are enveloped in transaction (@transactioned decorator).

    """

    def __init__(self, entities, mapping, log=LOGGER):
        """Initialize the archivist.

        entities - a list of ael entities to be archived.

        Subclasses need to implement:
            _check_entity
            _archive_entity
            _rollback_entities

        """
        self._log = log

        # finished == true if the run() method finished ok.
        self.finished = False

        if len(entities) > TRANSACTION_CHUNK_SIZE:
            raise Aggregation.GeneralError("An archivist must contain {0} entities at most.".format(TRANSACTION_CHUNK_SIZE))

        self._entities = entities if entities else []
        self._mapping = mapping if mapping else {}
        self.errors = []
        self._affected_entities = defaultdict(list)


    def _check_entity(self, entity):
        """Worker for entity checking."""

    def _check(self):
        """Fill self.errors with any errors.

        Returns boolean - is everything ok?

        """

        self.errors = []
        for entity in self._entities:
            check = self._check_entity(entity)
            try:
                iter(check)
            except TypeError:
                if check:
                    self.errors.append(check)
            else:
                self.errors.extend(check)

        return not self.errors

    def _archive_entity(self, entity):
        """Archive the given single entity.

        This is called from inside a transaction.

        """
        raise NotImplementedError()

    def _unarchive_entity(self, entity):
        """Unarchive the given single entity.

        This is called from inside a transaction in archived mode.

        """
        raise NotImplementedError()

    @transactioned(LOGGER)
    def _archive(self):
        """Archive all entities."""
        for entity in self._entities:
            self._archive_entity(entity)

    def run(self):
        """Run the aggregation of this chunk."""
        if self._check():
            try:
                self._archive()
                self.finished = True
            except:
                # Transaction aborted.
                self.finished = False
                raise
        else:
            # Chunk archiving failed.
            self.finished = False
            for e in self.errors:
                self._log.error(e)
            raise Aggregation.CheckError("There were errors in the archivist data.")

    def reset(self):
        """Reset this chunk - unarchive."""
        self._unarchive()

    @transactioned(LOGGER)
    def _unarchive(self):
        """Unarchive this all entities in this chunk."""
        for entity in self._entities:
            self._unarchive_entity(entity)

    def rollback(self):
        """Try to roll back the archiving."""
        self._safe_rollback()

        # If the safe rollback fails, this won't be executed.
        # Otherwise, erase the affected entities as they were rolled back.
        self._affected_entitites = defaultdict(list)

    @transactioned(LOGGER)
    def _safe_rollback(self):
        """The transactioned rollback method."""
        self._rollback_entities()

    def _rollback_entities(self):
        """The rollback logic itself."""
        raise NotImplementedError()

    def summary(self):
        """Return a summary of affected entities for this chunk."""
        return dict_list_lengths(self._affected_entities)

    def count(self):
        """Get the count of entities in this batch.

        This does not contain linked entities (addinfos etc).

        """
        return len(self._entities)

class TradeArchivist(Archivist):
    """A general trade-based archivist.

    Contains methods common to trade oriented archiving.

    """

    def _set_entity_archived(self, trade_clone, archive_flag):
        """Set archived or nonarchived flag on the trade and it's linked objects.

        This requires a clone of the ael trade entity and does not commit any
        changes. Returns a bool flag indicating whether the trade needs to be
        commited afterwards.

        """

        if trade_clone.aggregate != 0:
            msg = "Cannot archive an aggregate trade: {0}."
            raise Aggregation.CheckError(msg.format(trade_clone.trdnbr))

        archive_flag = 1 if archive_flag else 0

        changed = False

        linked = TradeAggregation.get_all_linked(trade_clone)

        # Archive the linked objects.
        for key, data in linked.iteritems():
            for value in data:
                if value.archive_status != archive_flag:
                    changed = True
                    value = value.clone()
                    value.archive_status = archive_flag
                    self._affected_entities[key].append(value)

        # Archive the trade itself and link it to the cash-posting trade.
        if trade_clone.archive_status != archive_flag:
            trade_clone.archive_status = archive_flag
            changed = True

        if changed:
            trade_clone.commit()
            self._affected_entities['trades'].append(trade_clone)

        return changed

    def _rollback_entities(self):
        """Rollback all the trades in this chunk."""
        for key in TradeAggregation.LINKED_OBJECTS:
            for value in self._affected_entities[key]:
                value = value.clone()
                value.archive_status = 0

        for t in self._affected_entities['trades']:
            t = t.clone()
            t.archive_status = 0
            t.aggregate_trdnbr = None
            t.commit()


class TradeArchivistMO(TradeArchivist):
    """Trade-specific chunk archivist."""
    def __init__(self, entities, mapping, log=LOGGER):
        """Initialize with the input files."""
        super(TradeArchivistMO, self).__init__(entities, mapping, log)

    def _check_entity(self, trade):
        """Worker checking one trade."""
        errors = []
        if trade.aggregate_trdnbr:
            errors.append("Trade {0} is aggregated, cannot archive.".format(trade.trdnbr))
        if trade.archive_status != 0:
            errors.append("Trade {0} is already archived.".format(trade.trdnbr))

        agg_trade = ael.Trade[self._mapping[trade.trdnbr]]
        trd_prf = trade.prfnbr
        agg_prf = agg_trade.prfnbr
        if agg_prf != trd_prf:
            msg = "Trade portfolio {1} is different from cash-posting trade portfolio {2}."
            errors.append(msg.format(trade.trdnbr, trd_prf.prfid, agg_prf.prfid))

        trd_cpty = trade.counterparty_ptynbr
        agg_cpty = agg_trade.counterparty_ptynbr
        if agg_cpty != trd_cpty:
            msg = "Trade counterparty {1} is different from cash-posting trade counterparty {2}."
            errors.append(msg.format(trade.trdnbr, trd_cpty.ptyid, agg_cpty.prfid))

        return errors

    def _set_entity_aggregated(self, trade, archive_flag):
        """Archives the entity and sets the aggregate trade link."""
        trade = trade.clone()
        changed = self._set_entity_archived(trade, archive_flag=archive_flag)
        if changed:
            if archive_flag:
                trade.aggregate_trdnbr = self._mapping[trade.trdnbr]
            else:
                trade.aggregate_trdnbr = None
            trade.commit()

    def _archive_entity(self, trade):
        """Archive the trade."""
        self._set_entity_aggregated(trade, archive_flag=True)

    def _unarchive_entity(self, trade):
        """Unarchive the trade."""
        self._set_entity_aggregated(trade, archive_flag=False)
