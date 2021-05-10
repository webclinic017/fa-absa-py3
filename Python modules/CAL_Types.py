def enum(**enums):
    return type('Enum', (), enums)

Clas_Flag = enum(Cancelled = 'C', Amended = 'A', Late = 'L', New = 'N')

class CalTrade(object):
    """Represents a CAL trade. """
    
    def __init__(self, clas_flag_enum):

        self.clas_flag = clas_flag_enum
        self.trade_date = ""
        self.book_id = ""
        self.book_name = ""
        self.book_system = ""
        self.orgin_trd_sys = ""
        self.trade_id = ""
        self.is_otc = ""
        self.settlement_date = ""
        self.version_number = ""
        self.event_entry_time = ""
        self.event_entry_location = ""
        self.pv = ""
        self.pv_delta = ""
        self.trade_quantity = ""
        self.trade_price = ""
        self.trade_side = ""
        self.trade_rate = ""
        self.trade_updater_gid = ""
        self.trade_updater_AB = ""
        self.trade_booked_by_gid = ""
        self.trade_booked_by_AB = ""
        self.counterparty_id = ""
        self.currency = ""
        self.region_code = ""
        self.amended_field = ""
        self.old_value = ""
        self.new_value = ""
        self.book_main_trader = ""
        self.business_date = ""
        self.capacity_code = ""
        self.trade_type = ""
        self.product_type = ""
        self.product_description = ""
        self.product_description_type = ""
        self.activity_ind = ""
	self.underlying_instrument = ""
        
    
    def get_csv_row(self):
        
        csv_row = []
        amended_field_string = ""
        old_value_string = ""
        new_value_string = ""

        csv_row.append(self.trade_date)
        csv_row.append(self.book_id)
        csv_row.append(self.book_name)
        csv_row.append(self.book_system)
        csv_row.append(self.orgin_trd_sys)
        csv_row.append(self.trade_id)
        csv_row.append(self.settlement_date)
        csv_row.append(self.version_number)
        csv_row.append(self.event_entry_time)
        csv_row.append(self.clas_flag)
        csv_row.append(self.pv)
        csv_row.append(self.pv_delta)
        csv_row.append(self.trade_quantity)
        csv_row.append(self.trade_price)
        csv_row.append(self.trade_side)
        csv_row.append(self.trade_rate)
        csv_row.append(self.trade_updater_gid)
        csv_row.append(self.trade_updater_AB)
        csv_row.append(self.trade_booked_by_gid)
        csv_row.append(self.trade_booked_by_AB)
        csv_row.append(self.counterparty_id)
        csv_row.append(self.currency)
        csv_row.append(self.is_otc)
        csv_row.append(self.region_code)
        
        pipe_start = 1
        for i in range(len(self.amended_field) - 1):
            self.amended_field.insert(pipe_start, '|')
            self.old_value.insert(pipe_start, '|')
            self.new_value.insert(pipe_start, '|')
            pipe_start += 2
        
        for i in range(len(self.amended_field)):
            amended_field_string += self.amended_field[i]
            old_value_string += self.old_value[i]
            new_value_string += self.new_value[i]
            
        csv_row.append(amended_field_string)
        csv_row.append(old_value_string)
        csv_row.append(new_value_string)
        
        csv_row.append(self.event_entry_location)
        csv_row.append(self.business_date)
        csv_row.append(self.capacity_code)
        csv_row.append(self.trade_type)
        csv_row.append(self.product_type)
        csv_row.append(self.product_description)
        csv_row.append(self.product_description_type)
        csv_row.append(self.activity_ind)
	csv_row.append(self.underlying_instrument)

        return csv_row
