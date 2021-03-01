from flask_table import Table, Col, LinkCol


class TreasureTable(Table):
    """
    treasure hunt table
    """
    classes = ['table']
    id = Col('Id', show=False)
    name = Col('Name')
    description = Col('Description')
    time = Col('Time (Minutes)')
    is_active = Col('Active')
    activate = LinkCol('Toggle','treasure.activate', url_kwargs=dict(id='id'))
    edit = LinkCol('Edit', 'treasure.edit', url_kwargs=dict(id='id'))