"""----------------------------------------------------------------------------
MODULE
    FCashSettlementCalculator : FCashSettlementCalculator contains the logic for calculating the MT type for cash settlements.

FUNCTION
    get_applicable_mt_type()
        Returns the applicable mt types for a give mt type as input

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

MTMapping_Settlement = \
{
    '103':      [
                    {'Amount':'<0', 'CPType':'Client',  'DeliveryType':'!Delivery versus Payment',  'IsCOV':'False'},
                    {'Amount':'<0', 'CPType':'Broker',  'HasBIC':'False', 'DeliveryType':'!Delivery versus Payment',    'IsCOV':'False'}
                ],

    '199':      [
                    {
                        'Amount':'<0', 'CPType':'Client',  'Relation':'Good Value',  'Status':'!Pending Cancellation','TARGET2':'False',
                        'EBA':'False','DeliveryType':'!Delivery versus Payment', 'IsCOV':'False'
                    },
                    {
                        'Amount':'<0', 'CPType':'Broker',  'HasBIC':'False',  'Relation':'Good Value',  'Status':'!Pending Cancellation',
                        'TARGET2':'False',  'EBA':'False','DeliveryType':'!Delivery versus Payment', 'IsCOV':'False'
                    }
                ],

    '192':      [
                    { 'Amount':'<0',  'CPType':'Client',  'Relation':'Cancellation', 'DeliveryType':'!Delivery versus Payment', 'IsCOV':'False'},
                    { 'Amount':'<0',  'CPType':'Broker',  'HasBIC':'False',   'Relation':'Cancellation','DeliveryType':'!Delivery versus Payment', 'IsCOV':'False'},
                    { 'Amount':'<0',  'CPType':'Client',   'Relation':'Good Value',   'Status':'Pending Cancellation', 'TARGET2':'False',
                        'EBA':'False',  'DeliveryType':'!Delivery versus Payment', 'IsCOV':'False'
                    },
                    { 'Amount':'<0',  'CPType':'Broker',  'HasBIC':'False', 'Relation':'Good Value',  'Status':'Pending Cancellation', 'TARGET2':'False',
                        'EBA':'False', 'DeliveryType':'!Delivery versus Payment', 'IsCOV':'False'
                    }
                ],

    '200':      [
                    {'Amount':'<0', 'DeliveryType':'!Delivery versus Payment', 'TradeType':'Account Transfer'}
                ],


    '202':      [
                    {'Amount':'<0','CPType':'Counterparty','DeliveryType':'!Delivery versus Payment', 'IsMX':'False', 'IsThirdPartyFX':'False'},
                    {'Amount':'<0','CPType':'Broker', 'HasBIC':'True', 'DeliveryType':'!Delivery versus Payment', 'IsMX':'False', 'IsThirdPartyFX':'False'}
                ],

    'PACS009':
                [
                    {'Amount':'<0','CPType':'Counterparty','DeliveryType':'!Delivery versus Payment', 'IsMX':'True'},
                    {'Amount':'<0','CPType':'Broker', 'HasBIC':'True', 'DeliveryType':'!Delivery versus Payment', 'IsMX':'True'}
                  ],

    '210':      [
                    {'Amount':'>0', 'Relation':'!Cancellation', 'NotifyReceipt':'True', 'TradeType':'!Account Adjustment', 'IsThirdPartyFX':'False', 'IsMX':'False'}
                ],

    'CAMT057':
                [
                    {'Amount':'>0', 'Relation':'!Cancellation', 'NotifyReceipt':'True', 'TradeType':'!Account Adjustment', 'IsThirdPartyFX':'False', 'IsMX':'True'}
                ],

    '292':      [
                    {'Amount':'<0', 'CPType':'Counterparty', 'Relation':'Cancellation', 'DeliveryType':'!Delivery versus Payment',  'IsThirdPartyFX':'False'},
                    {'Amount':'<0', 'CPType':'Broker', 'HasBIC':'True', 'Relation':'Cancellation', 'DeliveryType':'!Delivery versus Payment',  'IsThirdPartyFX':'False'},
                    {'Amount':'<0', 'CPType':'Counterparty', 'Relation':'Good Value', 'Status':'Pending Cancellation', 'TARGET2':'False', 'EBA':'False',
                     'DeliveryType':'!Delivery versus Payment', 'IsThirdPartyFX':'False'},
                    {'Amount':'<0', 'CPType':'Broker', 'HasBIC':'True', 'Relation':'Good Value', 'Status':'Pending Cancellation', 'TARGET2':'False', 'EBA':'False',
                     'DeliveryType':'!Delivery versus Payment', 'IsThirdPartyFX':'False'},
                    {'Amount':'>0',  'Relation':'Cancellation', 'NotifyReceipt':'True', 'IsThirdPartyFX':'False'}
                ],

    '299':      [
                    {'Amount':'<0', 'CPType':'Counterparty', 'Relation':'Good Value', 'Status':'!Pending Cancellation', 'TARGET2':'False', 'EBA':'False',
                     'DeliveryType':'!Delivery versus Payment'},
                    {'Amount':'<0', 'CPType':'Broker', 'HasBIC':'True', 'Relation':'Good Value', 'Status':'!Pending Cancellation', 'TARGET2':'False', 'EBA':'False',
                     'DeliveryType':'!Delivery versus Payment'},
                ],


    '202COV':   [
                    {'Amount':'<0', 'CPType':'Client',  'DeliveryType':'!Delivery versus Payment',  'IsCOV':'True'},
                    {'Amount':'<0', 'CPType':'Broker',  'HasBIC':'False',   'DeliveryType':'!Delivery versus Payment',  'IsCOV':'True'}
                ],


    '299COV':      [
                    {
                        'Amount':'<0', 'CPType':'Client',  'Relation':'Good Value',  'Status':'!Pending Cancellation','TARGET2':'False',
                        'EBA':'False','DeliveryType':'!Delivery versus Payment', 'IsCOV':'True'
                    },
                    {
                        'Amount':'<0', 'CPType':'Broker',  'HasBIC':'False',  'Relation':'Good Value',  'Status':'!Pending Cancellation',
                        'TARGET2':'False',  'EBA':'False','DeliveryType':'!Delivery versus Payment', 'IsCOV':'True'
                    }
                ],


    '292COV':      [
                    { 'Amount':'<0',  'CPType':'Client',  'Relation':'Cancellation', 'DeliveryType':'!Delivery versus Payment', 'IsCOV':'True'},
                    { 'Amount':'<0',  'CPType':'Broker',  'HasBIC':'False',   'Relation':'Cancellation','DeliveryType':'!Delivery versus Payment', 'IsCOV':'True'},
                    { 'Amount':'<0',  'CPType':'Client',   'Relation':'Good Value',   'Status':'Pending Cancellation', 'TARGET2':'False',
                        'EBA':'False',  'DeliveryType':'!Delivery versus Payment', 'IsCOV':'True'
                    },
                    { 'Amount':'<0',  'CPType':'Broker',  'HasBIC':'False', 'Relation':'Good Value',  'Status':'Pending Cancellation', 'TARGET2':'False',
                        'EBA':'False', 'DeliveryType':'!Delivery versus Payment', 'IsCOV':'True'
                    },
                    {'Amount':'<0', 'CPType':'Client',  'Status':'Pending Cancellation', 'DeliveryType':'!Delivery versus Payment',  'IsCOV':'True'},
                    {'Amount':'<0', 'CPType':'Broker',  'Status':'Pending Cancellation', 'HasBIC':'False',   'DeliveryType':'!Delivery versus Payment',  'IsCOV':'True'}
                ],

    '304':      [
                    {'Amount':'<0','DeliveryType':'!Delivery versus Payment', 'IsMX':'False', 'IsThirdPartyFX':'True'},
                    {'Amount':'<0', 'HasBIC':'True', 'DeliveryType':'!Delivery versus Payment', 'IsMX':'False', 'IsThirdPartyFX':'True'},
                    {'Amount':'<0', 'Relation':'Cancellation', 'DeliveryType':'!Delivery versus Payment',  'IsThirdPartyFX':'True'},
                    {'Amount':'<0','HasBIC':'True', 'Relation':'Cancellation', 'DeliveryType':'!Delivery versus Payment',  'IsThirdPartyFX':'True'},
                    {'Amount':'<0','Relation':'Good Value', 'Status':'Pending Cancellation', 'TARGET2':'False', 'EBA':'False',
                     'DeliveryType':'!Delivery versus Payment', 'IsThirdPartyFX':'True'},
                    {'Amount':'<0','HasBIC':'True', 'Relation':'Good Value', 'Status':'Pending Cancellation', 'TARGET2':'False', 'EBA':'False',
                     'DeliveryType':'!Delivery versus Payment', 'IsThirdPartyFX':'True'},
                    {'Amount':'>0',  'Relation':'Cancellation', 'NotifyReceipt':'True', 'IsThirdPartyFX':'True'}
                ]

}


def get_applicable_mt_type(acm_object, mt_type):
    """get applicable mt type list for the mt type"""
    import FCashOutMain
    import FSwiftWriterUtils
    import FSwiftMTCalculatorHook

    ret_list = []
    msg_supported = False
    msg_type = FSwiftWriterUtils.swift_format_of_message(mt_type)
    if msg_type == 'MT':
        if "MT%s" % str(mt_type) in FCashOutMain.SUPPORTED_MT_MESSAGE:
            msg_supported = True
    elif msg_type == 'MX':
        if mt_type in FCashOutMain.SUPPORTED_MX_MESSAGE:
            msg_supported = True

    if msg_supported:
        # If the user has defined mt_type specific function in FSwiftMTCalculatorHook use that function
        applicable_mt_type_func = getattr(FSwiftMTCalculatorHook, 'get_applicable_mt_type_%s' % str(mt_type), None)
        if applicable_mt_type_func:
            ret_list = applicable_mt_type_func()
        else:
            import FSwiftMLUtils
            if mt_type == '202COV':
                ret_list = ['103', '202COV']

            elif mt_type in ['199', '299', '299COV']:  # Pay Good Val
                child_settlement = acm_object.Children()
                if child_settlement:
                    child_settlement = child_settlement[0]

                    child_settlement_mt_type = str(FSwiftMLUtils.calculate_mt_type_from_acm_object(child_settlement))

                    if child_settlement_mt_type == '202COV':
                        ret_list = ['103', '202COV', '199-103', '299-202COV']
                    else:
                        pay_good_val_mt = mt_type + '-' + str(child_settlement_mt_type)
                        ret_list = [child_settlement_mt_type, pay_good_val_mt]

            elif mt_type in ['192', '292', '292COV']:  # Cancellation
                #sett status is pend_canc
                if acm_object.Status() != 'Pending Cancellation':
                    child_settlement = acm_object.Children()[0]
                    acm_object = child_settlement

                ext_objs = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_object,
                                                                       integration_type='Outgoing', all_records=True)
                for ext_obj in ext_objs:
                    mt_type_temp = mt_type
                    msg_typ = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(ext_obj)
                    bpr = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(ext_obj)
                    if ext_obj and bpr:
                        if bpr and bpr.CurrentStateName() in ['Acknowledged', 'Sent']:
                            if mt_type == '292COV' and msg_typ[2:] in ['103', '199']:
                                mt_type_temp = '192'
                            canc_mt_type = mt_type_temp[:3] + '-' + msg_typ[2:]
                            if canc_mt_type not in ret_list:
                                ret_list.append(canc_mt_type)

        if not ret_list:
            ret_list = [mt_type]

    return ret_list


