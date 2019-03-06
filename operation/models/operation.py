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
	m_patient_full_name = fields.Char(string="Nom avec la civilité 'M.' ou 'Mme.'")
	
	m_message = fields.Text(string="Message du formulaire")
	m_baldness = fields.Many2one('graft.baldness', string="Cas")
	m_baldness_image = fields.Binary(compute="_compute_image", store=True, string="Niveau de calvitie estimé par le patient")
	

	#medecin et relatives
	m_first_doctor = fields.Many2one('hr.employee', string="Médecin 1")
	m_first_doctor_time = fields.Selection([("half", "Demi-journée"), ("full", "Journée")], string="Temps opération médecin 1")
	m_second_doctor = fields.Many2one('hr.employee', string="Médecin 2")
	m_second_doctor_time = fields.Selection([("half", "Demi-journée"), ("full", "Journée")], string="Temps opération médecin 2")
	m_first_doctor_name = fields.Char(related='m_first_doctor.name', store=False, readonly=True)
	m_second_doctor_name = fields.Char(related='m_second_doctor.name', store=False, readonly=True)

	#dates
	m_operation_date_1 = fields.Datetime(string="Date prévue de l'opération")
	m_operation_date_2 = fields.Datetime()
	m_preoperative_consultation = fields.Datetime(string="Consultation préopératoire")

	#provenance du patient
	m_patient_origin = fields.Selection([("lisboa", "Lisbonne"), ("arpega", "Site web ARPEGA"), ("jalis", "Site web JALIS"), ("ehi", "Site web EHI"), ("facebook", "Facebook"), ("instagram", "Instagram"), ("greg", "Greg"), ("prescriber", "Prescripteur")], string="Origine du patient")
	m_prescriber_name = fields.Char(string="Nom du prescripteur")
	m_commission = fields.Boolean(default=False, string="Avec commission")
	m_acompte = fields.Boolean(default=False, string="Acompte patient", track_visibility='onchange')
	m_payment_method = fields.Selection([("transfer", "Virement"), ("paypal", "Paypal"), ("cheque", "Chèque")], default="transfer", string="Moyen de paiement")

	#greffons & interventions
	m_graft_number = fields.Integer(string="Nombre de greffons")
	m_other_intervention = fields.Boolean(default=False, string="Autres interventions")
	m_intervention_number = fields.Integer(string="Nombre d'interventions")
	m_intervention_date = fields.Text(string="Date des interventions")

	#options
	m_prp = fields.Selection([("invoiced", "PRP facturé"), ("not_invoiced", "PRP non facturé")], string="PRP")
	m_prp_amount = fields.Integer(string="Montant PRP facturé")
	m_srv = fields.Boolean(string="Supplément sans rasage visible SRV", default=False)
	m_srvzd = fields.Boolean(string="Supplément sans rasage visible SRVZD", default=False)
	m_extra_graft = fields.Integer(string="Greffons supplémentaires")

	#files
	m_consentement_eclaire_filename = fields.Char(string="Consentement éclairé")
	m_consentement_eclaire = fields.Binary(string="Consentement éclairé (binaires)")
	m_engagement_qualite_filename = fields.Char(string="Engagement qualité")
	m_engagement_qualite = fields.Binary(string="Engagement qualité (binaires)")
	m_exit_permit_filename = fields.Char(string="Autorisation de sortie")
	m_exit_permit = fields.Binary(string="Autorisation de sortie (binaires)")
	m_devis_filename = fields.Char(string="Devis")
	m_devis = fields.Binary(string="Devis (binaires)")
	m_analyse_sanguine_filename = fields.Char(string="Analyse sanguine")
	m_analyse_sanguine = fields.Binary(string="Analyse sanguine (binaires)", track_visibility='onchange')
	m_questionnaire_filename = fields.Char(string="Questionnaire médical")
	m_questionnaire = fields.Binary(string="Questionnaire médical (binaires)", track_visibility='onchange')
	m_pre_instruction_filename = fields.Char(string="Instructions préopératoires")
	m_pre_instruction = fields.Binary(string="Instructions préopératoires (binaires)")
	m_post_instruction_filename = fields.Char(string="Instructions postopératoires")
	m_post_instruction = fields.Binary(string="Instructions postopératoires (binaires")
	m_prescription_filename = fields.Char(string="Prescription des médicaments")
	m_prescription = fields.Binary(string="Prescription des médicaments (binaires)")
	m_donor_neck_filename = fields.Char(string="Zone donneuse (nuque)")
	m_donor_neck = fields.Binary(string="Zone donneuse (nuque) (binaires)")
	m_donor_side_filename = fields.Char(string="Zone donneuse (côté)")
	m_donor_side = fields.Binary(string="Zone donneuse (côté) (binaires)")
	m_treat_face_filename = fields.Char(string="Zone à traiter (face)")
	m_treat_face = fields.Binary(string="Zone à traiter (face) (binaires)")
	m_treat_side_filename = fields.Char(string="Zone à traiter (profil)")
	m_treat_side = fields.Binary(string="Zone à traiter (profil) (binaires)")
	m_treat_top_filename = fields.Char(string="Zone à traiter (dessus)")
	m_treat_top = fields.Binary(string="Zone à traiter (dessus) (binaires)")

	#partie patient
	m_patient = fields.Many2one('res.partner', string="Patient", required=True)
	m_patient_name = fields.Char(related='m_patient.name', store=False, readonly=True)
	m_patient_mail = fields.Char(related='m_patient.email', string="Email", store=False, readonly=True)
	m_patient_yo = fields.Integer(related='m_patient.m_years_old', string="Âge", store=False, readonly=True)
	m_patient_gender = fields.Selection(related='m_patient.m_gender', string="Sexe", store=False, readonly=True)
	m_patient_mobile = fields.Char(related='m_patient.mobile', string="Mobile", store=False, readonly=True)
	m_patient_language = fields.Selection(related="m_patient.m_language", string="Langue du patient", store=False, readonly=True)

	#hébergement
	m_hotel = fields.Boolean(string="Hébergement compris dans le devis")
	m_hotel_person_number = fields.Integer(string="Nombre de personnes comprises dans l'hébergement")
	m_reservation = fields.Boolean(string="Réservation de l'hôtel", track_visibility='onchange')
	m_hotel_name = fields.Char(string="Nom de l'hôtel")


	#stage
	m_stage_selection = fields.Selection([("asking","Demande de devis"), ("fileOk","Dossier renseigné"), ("sending","Envoie du devis"), ("validated","Accord & Date validée"), ("consultation", "Consultation préopératoire"), ("postop", "Suivi post op"), ("other", "Autres interventions"), ("closed", "Fermé")], string="Etat d'avancement", default="asking", group_expand="_read_group_stage_ids", store=True, track_visibility='onchange')


	@api.depends('m_baldness')
	def _compute_image(self):
		for operation in self:
			operation.m_baldness_image = operation.m_baldness.m_image

	@api.model
	def _read_group_stage_ids(self, stages, domain, order):
		"""This function allows the kanban view to get all the known file status (even if the status doesn't contain any graft)
		
		Args:
		    stages (TYPE): Not used
		    domain (TYPE): Not used
		    order (TYPE): Not used
		
		Returns:
		    Array[]: Over the possible stages
		"""
		return (["asking", "fileOk", "sending", "validated", "consultation", "postop", "other", "closed"])


	@api.model
	def create(self, values):
		"""Overrides the create default method in order to allow a mail sending when a new ticket is recorded
		
		Args:
		    values (tab): Fields of Operation class (at least the required fields) 
		
		Returns:
		    Operation: Class
		"""

		# Override the original create function for the this model
		record = super(Operation, self).create(values)

		#mail sending to the caller
		template_env = self.env['mail.template']
		domain = []
		
		if record.m_patient_language == 'en':
			domain = ['&', ('model_id.model', '=', 'graft.operation'), ('name', 'like', '{en}')]
		elif record.m_patient_language == 'fr':
			domain = ['&', ('model_id.model', '=', 'graft.operation'), ('name', 'like', '{fr}')]
		else:
			domain = ['&', ('model_id.model', '=', 'graft.operation'), ('name', 'like', '{pt}')]

		if len(template_env.search(domain)) > 0:
			mail_template = template_env.search(domain)[0]
			mail_template.send_mail(record.id)
		
		return record

	@api.depends('m_patient_name')
	def _compute_name(self):
		"""Since m_name and m_client_nom_civil are not input fields, they are computed by this function with client information
		"""
		for operation in self:
			if operation.m_patient_name:
				operation_environment = self.env['graft.operation']
				last_operation = operation_environment.sudo().search([], order="id desc", limit=1)

				last_id = int(last_operation.id) if last_operation else 0
				operation.m_name = "Devis " + str(last_id) + " - " + operation.m_patient_name
				operation.m_patient_full_name = ' '.join(['M.', operation.m_patient_name]) if operation.m_patient.m_gender == 'man' else ' '.join(['Mme.', operation.m_patient_name])