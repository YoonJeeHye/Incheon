from wtforms import Form, StringField, SelectField
class GymSearchForm(Form):
    choices = [('gCategory', 'gCategory')]
    select = SelectField('Search for gym:', choices=choices)
    search = StringField('')