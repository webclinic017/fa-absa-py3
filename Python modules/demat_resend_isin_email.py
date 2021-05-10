import acm
import ael
from at_ael_variables import AelVariableHandler
from demat_isin_mgmt_confirmation import resend_isin_report

def save_email_hook(selected_variable):
    save_email = ael_variables.get('save_email')
    output_path = ael_variables.get('output_path')
    output_path.enabled = save_email.value
    output_path.mandatory = save_email.value

ael_variables = AelVariableHandler()

ael_variables.add(
    'instrument_id',
    label='Instrument ID',
    alt='Instrument ID'
)

ael_variables.add_output_file(
    'output_path',
    label='Output Path',
    alt='Output path for email.'
)

ael_variables.add_bool(
    'save_email',
    label='Save Email',
    default=True,
    alt="Save email localy",
    hook=save_email_hook
)

def ael_main(parameters):
    instrument_id = parameters['instrument_id']
    save_email = ael_variables.get('save_email')
    output_path = parameters['output_path']

    resend_isin_report(
        instrument_id,
        save_mail=save_email,
        path=str(output_path)
    )
