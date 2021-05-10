"""----------------------------------------------------------------------------
MODULE:
    FMT299NarrativeOut

DESCRIPTION:
    OPEN EXTENSION MODULE
    FMT299Narrative class for user customization.
    This class can be populated using either swift data or an acm object.
    See FMT699OutBase for extracting the values from acm

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""

import FMTx99OutBase
import FSwiftWriterLogger
import FCashOutUtils
import FSwiftMTx99Utils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')


class FMT299Narrative(FMTx99OutBase.FMTx99Base):

	def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
		swift_message_type = 'MT299Narrative'
		super(FMT299Narrative, self).__init__(acm_obj, swift_message_type, swift_obj, swift_metadata_xml_dom)


	# To override existing mappings use below methods to write your own logic
	"""
	narrative_79
	related_reference_21
	transaction_reference_20
	get_user_data
	"""


class FMT299NarrativeMessageHeader(FMTx99OutBase.FMTx99OutBaseMessageHeader):

	def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
		self.acm_obj = acm_obj
		self.swift_msg_tags = swift_msg_tags
		self.mt_type = '299'
		super(FMT299NarrativeMessageHeader, self).__init__(acm_obj, self.mt_type, swift_msg_tags)

	# To override existing mappings use below methods to write your own logic
	"""
	application_id
	service_id
	sender_logical_terminal_address
	session_number
	sequence_number
	input_or_output
	message_priority
	message_type
	receiver_logical_terminal_address
	delivery_monitoring
	non_delivery_notification_period
	service_identifier
	banking_priority_code
	message_user_reference
	validation_flag
	"""

	def logical_terminal_address(self, bic_code, lt_code):
		""" create terminal address for the party
		:param bic_code: bic of the party
		:param lt_code: code for the party
		:return:
		"""
		terminal_address = ""
		branch_code = "XXX"
		if bic_code:
			if len(str(bic_code)) == 8:
				terminal_address = str(bic_code) + lt_code + branch_code
			elif len(str(bic_code)) == 11:
				branch_code = bic_code[8:]
				terminal_address = str(bic_code[:8]) + lt_code + branch_code
			else:
				raise Exception("Invalid BIC <%s>)" % bic_code)
		return terminal_address

	def receiver_logical_terminal_address(self):
		"""receiver logical terminal address"""
		receivers_bic = None
		if self.acm_obj.RecordType() == "Settlement":
			receivers_bic = FCashOutUtils.get_receivers_bic(self.acm_obj)
		elif self.acm_obj.RecordType() == "Party":
			receivers_bic = FSwiftMTx99Utils.get_bic_from_party(self.acm_obj)
		elif self.acm_obj.RecordType() == "Trade":
			receivers_bic = FMTx99OutBase.get_value_from_bpr_diary(self.acm_obj, "MT" + self.mt_type, 'ReceiverBIC')
		if not receivers_bic:
			raise Exception("RECEIVER_BIC is a mandatory field for Swift message header")
		terminal_address = self.logical_terminal_address(receivers_bic, "X")
		return terminal_address


class FMT299NarrativeNetworkRules(FMTx99OutBase.FMTx99OutBaseNetworkRules):

	def __init__(self, swift_message_obj, swift_message, acm_obj):
		super(FMT299NarrativeNetworkRules, self).__init__(swift_message_obj, swift_message, acm_obj)
