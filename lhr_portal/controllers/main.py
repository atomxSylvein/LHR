import base64
from odoo import http
from odoo.http import request

from odoo.addons.website.controllers.main import Website

class Main(Website):

	#homepage
	"""@http.route('/', type='http', auth='public', website=True)
	def index(self, **kw):
		return request.render('lhr_portal.accueil', {} )"""
	@http.route('/page', auth="public", website=True)
	def blank(self):
		return request.render('lhr_portal.blank', {})


	@http.route('/<lang>/formulaire-contact', auth="public", website=True, csrf=False)
	def formulaire_devis(self, lang=None, **post):
		#récupération des pays
		country_environment = request.env['res.country'] 
		countries = country_environment.sudo().search([])
		language = "fr" if lang == "fr_FR" else "en" if lang == "en_EN" else "pt"
		title = "Demande de devis" if language == "fr" else "Quote request" if language == "en" else "Orçamento personalizado"
		return request.render('lhr_portal.create_operation', { 'countries' : countries, 'lang':language, 'source':post.get('source'), 'title':title,} )


	@http.route('/success', type='http', auth='public', website=True)
	def create_devis(self, **post):

		contact_environment = request.env['res.partner']

		#do we have to create this contact
		fullname = ' '.join([post.get('lastname'), post.get('firstname')])

		domain = ['&', ('name', '=', fullname), ('email', '=', post.get('email'))]
		existing_contact = contact_environment.sudo().search(domain)

		contact_id = 0

		if not existing_contact :
			contact = contact_environment.sudo().create({
				'name': fullname,
				'phone': post.get('phone'),
				'mobile': post.get('mobile'),
				'street': post.get('street'),
				'zip': post.get('zip'),
				'city': post.get('city'),
				'email': str(post.get('email')),
				'country_id' : int(post.get('country')),
				'm_gender': 'man' if str(post.get('gender')) == 'man' else 'woman',
				'm_years_old': int(post.get('yo')),
				'm_language': post.get('lang'),
				'm_graft': False if str(post.get('grafted')) == "no" else True,
				'm_last_intervention': False if str(post.get('grafted')) == "no" else True,
				'm_intervention_type': 'fue' if str(post.get('grafted')) == "fue" else "fut" if str(post.get('grafted')) == "fut" else "",
			})
			contact_id = int(contact.id)
		else :
			contact_id = int(existing_contact.id)

		#determine baldness degree
		baldness_environment = request.env['graft.baldness']
		domain = ['&', ('m_gender', '=', post.get('gender')), ('m_case', '=', post.get('case'))]
		baldness_id = baldness_environment.sudo().search(domain)

		#determine origin
		origin = ""
		if post.get('source', False):
			_website = str(post.get('source')).split('.')[1]
			origin = "jalis" if _website == "lisboahair" else "arpega" if _website == "lisboa-hair" else "ehi" if _website == "ehi-company" else ""

		#then create new operation with status
		operation_environment = request.env['graft.operation']
		operation = operation_environment.sudo().create({
			'm_patient': contact_id,
			'm_message': post.get('message'),
			'm_baldness': int(baldness_id),
			'm_patient_origin' : origin, 
			'm_donor_neck_filename' : str(post.get('donor_neck').filename) if post.get('donor_neck',False) else None,
			'm_donor_neck' : base64.b64encode(post.get('donor_neck').read()) if post.get('donor_neck',False) else None,
			'm_donor_side_filename' : str(post.get('donor_side').filename) if post.get('donor_side',False) else None,
			'm_donor_side' : base64.b64encode(post.get('donor_side').read()) if post.get('donor_side',False) else None,
			'm_treat_face_filename' : str(post.get('treat_face').filename) if post.get('treat_face',False) else None,
			'm_treat_face' : base64.b64encode(post.get('treat_face').read()) if post.get('treat_face',False) else None,
			'm_treat_side_filename' : str(post.get('treat_side').filename) if post.get('treat_side',False) else None,
			'm_treat_side' : base64.b64encode(post.get('treat_side').read()) if post.get('treat_side',False) else None,
			'm_treat_top_filename' : str(post.get('treat_top').filename) if post.get('treat_top',False) else None,
			'm_treat_top' : base64.b64encode(post.get('treat_top').read()) if post.get('treat_top',False) else None,
		})
		return request.render('lhr_portal.success', {'source':post.get('source'),'lang':post.get('lang'),} )