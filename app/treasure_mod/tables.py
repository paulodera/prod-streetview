from flask_table import Table, Col, LinkCol


class TreasureTable(Table):
    """
    treasure hunt table
    """
    classes = ['table']
    id = Col('Id', show=False)
    name = Col('Name')
    description = Col('Description')
    time = Col('Time')
    is_active = Col('Active')
