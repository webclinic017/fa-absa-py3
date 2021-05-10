"""List of function to with Front Arena workbooks and sheets.

TODO:
    - Support vector and time-bucket columns
    - Create ``add_sheet`` and ``remove_sheet``?
"""
import acm

def _get_creators(sheet, context=acm.GetDefaultContext()):
    """Returns FColumnCreators for specific sheet.
    
    :param sheet: ACM object.
    :type sheet: ``FTradingSheet``
    :param context: Name of used context (default: Standard context)
    :type context: FExtensionContext
    :returns: FColumnCreators
    
    """
    ctx = acm.FColumnCreatorCreateContext(context)
    return sheet.ColumnCreatorCollection(ctx)

def _get_creator(creators, column, position=False):
    """Helper function to return column creator or position.
    
    :param sheet: ACM object.
    :type sheet: ``FTradingSheet``
    :param column: Column ID
    :type column: string (example: Interest Rate Yield Delta)
    :param context: Name of used context (default: Standard context)
    :type context: FExtensionContext
    :param position: If True, will return position index otherwise FColumnCreator
    :type position: boolean
    :returns: integer | FColumnCreator | None if column not found
    
    """
    # using while because FColumnCreators is not iterable
    ref_creator = None; i = 0
    while i < creators.Size():
        if creators.At(i).ColumnId() == acm.FSymbol(column):
            ref_creator = creators.At(i)
            break
        i += 1
    
    if ref_creator and not position:
        return ref_creator
    elif ref_creator and position:
        return i

    return None

def get_columns(sheet, context=acm.GetDefaultContext()):
    """Returns FArray containing strings of column IDs for specific context.
    
    :param sheet: ACM object.
    :type sheet: ``FTradingSheet``
    :param context: Name of used context (default: Standard context)
    :type context: FExtensionContext
    :returns: FArray
    
    """
    ctx = acm.FColumnCreatorCreateContext(context)
    return sheet.ColumnCollection(ctx)

def add_columns(sheet, columns, after=None, before=None, context=acm.GetDefaultContext()):
    """Adds ``columns`` to sheet depending on ``after`` or ``before`` options.
    Will append column to the end of a sheet by default.
    
    :param sheet: ACM object.
    :type sheet: ``FTradingSheet``
    :param columns: List of new column IDs
    :type columsn: list or tuple of strings
    :param after: New column will be added just behind this column
    :type after: string (example: Portfolio Total Profit and Loss)
    :param before: New column will be added just before this column
    :type before: string (example: Portfolio Unrealized Profit and Loss)
    :param context: Name of used context (default: Standard context)
    :type context: FExtensionContext
    :returns: integer with position
    
    """
    creators = _get_creators(sheet, context)
    ref_creator = _get_creator(creators, after or before)
    
    new_columns = acm.FArray()
    new_columns.AddAll(columns)
    
    new_creators = acm.GetColumnCreators(new_columns, context)

    i = 0
    while i < new_creators.Size():
        column_creator = new_creators.At(i)
        if ref_creator:
            if after:
                creators.InsertAfter(ref_creator, column_creator)
            elif before:
                creators.InsertBefore(ref_creator, column_creator)
        else:
            creators.Add(column_creator)
        i += 1
    
    sheet.SetColumnCreatorCollection(creators)
    sheet.Commit()

def remove_columns(sheet, columns, context=acm.GetDefaultContext()):
    """Removes ``column`` from sheet.
    
    :param sheet: ACM object.
    :type sheet: ``FTradingSheet``
    :param columns: List or tuple of columns to be removed
    :type columns: list or tuple of strings
    :param context: Name of used context (default: Standard context)
    :type context: FExtensionContext
    :returns: integer with position
    
    """
    creators = _get_creators(sheet, context)
    
    for column in columns:
        ref_creator = _get_creator(creators, column)
        if ref_creator:
            creators.Remove(ref_creator)
    
    sheet.SetColumnCreatorCollection(creators)
    sheet.Commit()

def add_column(sheet, column, after=None, before=None, context=acm.GetDefaultContext()):
    """Short-hand alias for ``add_columns``"""
    return add_columns(sheet, [column], after, before, context)

def remove_column(sheet, column, context=acm.GetDefaultContext()):
    """Short-hand alias for ``remove_columns``"""
    return remove_columns(sheet, [column], context=acm.GetDefaultContext())

def replace_column(sheet, old_column, new_column, context=acm.GetDefaultContext()):
    """Replaces ``old_column`` ID with ``new_column`` ID in specific sheet.
    
    :param sheet: ACM object.
    :type sheet: ``FTradingSheet``
    :param old_column: Old column ID
    :type old_column: string (example: Interest Rate Yield Delta)
    :param new_column: New column ID
    :type new_column: string (example: Price Delta Instrument)
    :param context: Name of used context (default: Standard context)
    :type context: FExtensionContext
    
    """
    creators = _get_creators(sheet, context)
    ref_creator = _get_creator(creators, old_column)
    new_creator = acm.GetColumnCreators(new_column, context).At(0)
    
    if ref_creator:
        creators.InsertAfter(ref_creator, new_creator)
        creators.Remove(ref_creator)
        sheet.SetColumnCreatorCollection(creators)
        sheet.Commit()
