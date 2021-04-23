"""----------------------------------------------------------------------------
MODULE:
    FSwiftMTx99Utils

DESCRIPTION:
    A module for utility methods used for processing all types of Narrative Messages.

CLASS:

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm
import FSwiftMLUtils
import FSwiftWriterLogger
import FSwiftConfirmationOutUtils
import FSwiftConfirmationUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SWIFTMTx99Utils', 'FNarrativeOut_Config')
swift_mtn99_out_msg_config = FSwiftMLUtils.Parameters('FMTx99Out_Config')
writer_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')


def get_party_reference_prefix():
	"""returns confirmation reference prefix"""
	if str(getattr(swift_mtn99_out_msg_config, 'FAP', "")) == "":
		return str(getattr(writer_config, 'FAP', "FAP"))
	return str(getattr(swift_mtn99_out_msg_config, 'FAP', None))


def get_trade_reference_prefix():
	"""returns confirmation reference prefix"""
	if str(getattr(swift_mtn99_out_msg_config, 'FAT', "")) == "":
		return str(getattr(writer_config, 'FAT', "FAT"))
	return str(getattr(swift_mtn99_out_msg_config, 'FAT', None))


def get_confirmation_reference_prefix():
	"""returns confirmation reference prefix"""
	if str(getattr(swift_mtn99_out_msg_config, 'FAC', "")) == "":
		return str(getattr(writer_config, 'FAC', "FAC"))
	return str(getattr(swift_mtn99_out_msg_config, 'FAC', None))


def get_bic_from_party(party):
	""" Method to retrieve BIC from party object """
	bic = ''
	for alias in party.Aliases():
		if alias.Type().Name() == 'SWIFT':
			bic = alias.Name()
	if not bic:
		bic = party.Swift()
	return bic


def get_settlement_reference_prefix():
	settle_prefix = None
	if str(getattr(swift_mtn99_out_msg_config, 'FAS', "")) == "":
		settle_prefix = str(getattr(writer_config, 'FAS', "FAS"))
	else:
		settle_prefix = str(getattr(swift_mtn99_out_msg_config, 'FAS', None))
	return settle_prefix


def get_mt_version_number(acm_obj, msg_typ):
	""" Get version number for MT699. Each new message version is incremented by 1. First message version number is 0.
	:param acm_obj: Settlement or confirmation object
	:return: int: version number for new MT699 message.
	"""
	version_number = 0
	try:
		if msg_typ in ['MT199', 'MT299']:
			msg_typ = msg_typ + 'Narrative'
		external_object = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj,
			integration_type='Outgoing',
			msg_typ=msg_typ,
			all_records=True)
		if external_object:
			version_number = len(external_object)
	except Exception as e:
		pass
	return version_number


def get_narrative_description(acm_obj, mt_type):
	""" Optional field 79 for n99 message
	:param acm_obj: Settlement or confirmation object
	:param mt_type: type of message
	:return:  str: narrative text
	"""
	narrative_text = 'This is narrative description'

	if mt_type:
		external_object = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj,
			integration_type='Outgoing',
			msg_typ=mt_type)
		if external_object:
			if not isinstance(external_object, list):
				external_object = [external_object]
			bpr = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(external_object[-1])
			if bpr:
				narrative_text = FSwiftMLUtils.get_parameters_from_bpr_state(bpr, 'Ready',
					'NarrativeText')

	return str(narrative_text)


def get_senders_bic_settlement(settlement):
	"""Returns SWIFT bic code of the Acquirer of the settlement.
	This field goes into {1: Basic Header Block} -- Address of the Sender"""

	swift_loopback = getattr(swift_mtn99_out_msg_config, 'SwiftLoopBack', 'None')
	sender_bic_loopback = getattr(swift_mtn99_out_msg_config, 'SenderBICLoopBack', 'None')
	if swift_loopback == 'None' and sender_bic_loopback == 'None':
		swift_loopback = getattr(writer_config, 'SwiftLoopBack', 'None')
		sender_bic_loopback = getattr(writer_config, 'SenderBICLoopBack', 'None')

	if swift_loopback and eval(swift_loopback) and eval(swift_loopback) == True and sender_bic_loopback and eval(
			sender_bic_loopback):
		senders_bic = eval(sender_bic_loopback)
	else:
		account = settlement.AcquirerAccountRef()
		if account and account.NetworkAlias():
			senders_bic = account.NetworkAlias().Alias()
		else:
			assert settlement.AcquirerAccountRef(), "The settlement has no acquirer account reference"
			assert settlement.AcquirerAccountRef().Party(), "The acquirer account referenced by the settlement has no party"
			senders_bic = account.Party().Swift()
	return senders_bic


def get_bic(confirmation, sender_receiver):
	""" Get sender's/receiver's bic """
	bic = None
	if str(getattr(swift_mtn99_out_msg_config, 'SwiftLoopBack', "")) == 'True':
		bic = str(getattr(swift_mtn99_out_msg_config, sender_receiver, ""))
	elif str(getattr(writer_config, 'SwiftLoopBack', "")) == 'True':
		bic = str(getattr(writer_config, sender_receiver, ""))
	elif str(sender_receiver) == 'SenderBICLoopBack':
		bic = confirmation.AcquirerAddress()
	elif str(sender_receiver) == 'ReceiverBICLoopBack':
		bic = confirmation.CounterpartyAddress()
	return bic


def get_senders_bic_confirmation(confirmation):
	""" Get the senders bic """
	return get_bic(confirmation, 'SenderBICLoopBack')


def get_receivers_bic_confirmation(confirmation):
	""" Get the receivers bic """
	return get_bic(confirmation, 'ReceiverBICLoopBack')


def get_receivers_bic_settlement(settlement):
	"""Returns SWIFT bic code of settlement receiver.
	This field goes into {2:Application Header Block} -- Receiver Information."""

	receiverBic = ''

	swift_loopback = getattr(swift_mtn99_out_msg_config, 'SwiftLoopBack', 'None')
	receiver_bic_loopback = getattr(swift_mtn99_out_msg_config, 'ReceiverBICLoopBack', 'None')
	if swift_loopback == 'None' and receiver_bic_loopback == 'None':
		swift_loopback = getattr(writer_config, 'SwiftLoopBack', 'None')
		receiver_bic_loopback = getattr(writer_config, 'ReceiverBICLoopBack', 'None')

	if swift_loopback and eval(swift_loopback) and eval(swift_loopback) == True and receiver_bic_loopback and eval(
			receiver_bic_loopback):
		receiverBic = eval(receiver_bic_loopback)
	else:
		acquireAccount = settlement.AcquirerAccountRef()
		counterPartyAccount = settlement.CounterpartyAccountRef()
		if counterPartyAccount:
			if settlement.CounterpartyAccountSubNetworkName() in ('TARGET2', 'EBA'):
				if counterPartyAccount.Bic2():
					receiverBic = counterPartyAccount.Bic2().Alias()
				elif counterPartyAccount.Bic():
					receiverBic = counterPartyAccount.Bic().Alias()
		if receiverBic == '':
			if acquireAccount:
				if acquireAccount.Bic():
					receiverBic = acquireAccount.Bic().Alias()

	return receiverBic


def get_message_version_number(fObject, is_free_text_msg=False):
	msg_version_number = fObject.VersionId()
	if is_free_text_msg:
		msg_version_number = str(msg_version_number) + 'F'
	return str(msg_version_number)

