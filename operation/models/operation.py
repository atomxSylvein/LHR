# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID

class Operation(models.Model):

	"""Core of this module. This class describes what is a graft operation
	
	Attributes:
	    m_all_day (boolean): Graft operation lasts all day
	    m_anesthesie (boolean): is anesthesia used or not
	    m_chirurgien (Many2one): Head surgeon of the operation
	    m_chirurgien_nom (str): Surgeon's name, not stored
	    m_client (Many2one): Customer/caller
	    m_client_age (Integer): Customer's age, not stored
	    m_client_genre (Selection): Customer's sex, not stored
	    m_client_mail (str): Customer's mail address, not stored
	    m_client_nom (str): Customer's name, not stored
	    m_client_nom_civil (str): Complete name of the customer
	    m_consentement_eclaire (file): Part of the graft file
	    m_date_prevu (TYPE): Planned date for the graft operation
	    m_engagement_qualite (file): Part of the graft file
	    m_hotel (boolean): is hotel stay included or not in the plan
	    m_message (str): message sent by the client
	    m_name (str): name of the file
	    m_nb_nuit_hotel (TYPE): number of night spent at the hotel
	    m_prp (boolean): is PRP included or not
	    m_stage_selection (Selection): Status of the file
	    m_zrnt (boolean): example of an action which can be performed during the graft operation
	"""
	
	_name = 'graft.operation'
	_rec_name = 'm_name'
	_inherit = ['mail.thread']

	m_name = fields.Char(compute='_compute_name', string="Nom de l'opération", store=True)
	m_client_nom_civil = fields.Char(string="Nom avec la civilité 'M.' ou 'Mme.'")
	m_chirurgien = fields.Many2one('hr.employee', string="Chirurgien")
	m_client = fields.Many2one('res.partner', string="Client", required=True)
	m_date_prevu = fields.Datetime(string="Date prévue de l'opération")
	m_message = fields.Text(string="Message du formulaire")
	m_all_day = fields.Boolean(string="L'opération dure toute la journée", required=True, default=True)

	#relative actions & hotel
	m_anesthesie = fields.Boolean(string="Utilisation d'anesthésique", default=False)
	m_prp = fields.Boolean(string="PRP", default=False)
	m_zrnt = fields.Boolean(string="Supplément zone receveuse non tondue", default=False)
	m_hotel = fields.Boolean(string="Hébergement compris dans le forfait", default=False)
	m_nb_nuit_hotel = fields.Integer(string="Nombre de nuits compris dans le forfait", default=0)
	
	#related fields
	m_chirurgien_nom = fields.Char(related='m_chirurgien.name', store=False, readonly=True)
	m_client_nom = fields.Char(related='m_client.name', store=False, readonly=True)
	m_client_mail = fields.Char(related='m_client.email', store=False, readonly=True)
	m_client_age = fields.Integer(related='m_client.x_years_old', store=False, readonly=True)
	m_client_genre = fields.Selection(related='m_client.x_gender', store=False, readonly=True)
	
	#files
	m_consentement_eclaire = fields.Binary(string="Consentement éclairé")
	m_engagement_qualite = fields.Binary(string="Engagement qualité")

	#stage
	m_stage_selection = fields.Selection([("brouillon","Demande de devis"), ("enCours","Dossier en cours de validation"), ("planifie","Opération validée"), ("archive","Archivé")], string="Statut du dossier", default="brouillon", group_expand="_read_group_stage_ids", store=True, track_visibility='onchange')


	@api.model
	def _read_group_stage_ids(self, stages, domain, order):
		"""This function allows the kanban view to get all the known file status (even if the status doesn't contain any graft)
		
		Args:
		    stages (TYPE): Not used
		    domain (TYPE): Not used
		    order (TYPE): Not used
		
		Returns:
		    Array[graft.stage]: Description
		"""
		return (["brouillon", "enCours", "planifie", "archive"])

	@api.one
	def plan_operation(self):
		self.write({'m_stage_selection':"planifie"})

	@api.model
	def create(self, values):
		"""Overrides the create default method in order to allow a mail sending when a new ticket is recorded
		
		Args:
		    values (tab): Fields of TicketManagement class (at least the required fields) 
		
		Returns:
		    TicketManagement: Class
		"""

		# Override the original create function for the this model
		record = super(Operation, self).create(values)

		#mail sending to the caller
		template_env = self.env['mail.template']
		mail_template = template_env.search([('model_id.model', '=', 'graft.operation')])[0]
		mail_template.send_mail(record.id)
		
		return record

	@api.depends('m_client_nom')
	def _compute_name(self):
		"""Since m_name and m_client_nom_civil are not input fields, they are computed by this function with client information
		"""
		for operation in self:
			if operation.m_client_nom:
				operation_environment = self.env['graft.operation']
				last_operation = operation_environment.sudo().search([], order="id desc", limit=1)

				last_id = int(last_operation.id) if last_operation else 0
				operation.m_name = "Devis " + str(last_id) + " - " + operation.m_client_nom
				operation.m_client_nom_civil = ' '.join(['M.', operation.m_client_nom]) if operation.m_client.x_gender == 'man' else ' '.join(['Mme.', operation.m_client_nom])