from odoo import models, fields, api

class ContactPlugin(models.Model):

	"""This class extends Project class and provides implements the projects statuses
	
	Attributes:
	    m_gender (selection): Man or woman
	    m_graft (bool): Is the patient already grafted
	    m_graft_number (int): Number of grafts
	    m_intervention_date (date): Date of previous operations
	    m_intervention_type (selection): FUE or FUT
	    m_language (selection): Patient language
	    m_last_intervention (bool): Has the patien already performed a graft operation
	    m_years_old (int): Patient's age
	"""
	
	_inherit = 'res.partner'
	m_gender = fields.Selection([("man","Homme"), ("woman","Femme")], default='man', string="Genre", translate=True)
	m_years_old = fields.Integer(string="Âge", default="", translate=True)
	m_graft = fields.Boolean(string="Déjà greffé", default=False, help="Le patient a t-il déjà eu recours à la greffe ?", translate=True)
	m_last_intervention = fields.Boolean(string="Interventions précédentes", default=False, translate=True)
	m_intervention_type = fields.Selection([("fue","FUE"), ("fut","FUT")], string="Type d'intervention", translate=True)
	m_graft_number = fields.Integer(string="Nombre de greffons", translate=True)
	m_intervention_date = fields.Char(string="Date de l'intervention")
	m_language = fields.Selection([('en', 'Anglais'), ('fr', 'Français'), ('pt', 'Portugais')], string="Langue", translate=True)