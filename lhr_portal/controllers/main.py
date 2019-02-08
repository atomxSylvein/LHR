import base64
from odoo import http
from odoo.http import request

from odoo.addons.website.controllers.main import Website

class Main(Website):

	#homepage
	"""@http.route('/', type='http', auth='public', website=True)
	def index(self, **kw):
		return request.render('lhr_portal.accueil', {} )"""

	@http.route('/formulaire-contact', auth='public', website=True)
	def formulaire_devis(self):
		#récupération des pays
		country_environment = request.env['res.country']
		countries = country_environment.sudo().search([])

		return request.render('lhr_portal.create_operation', { 'countries' : countries, } )

	@http.route('/lhr-created', type='http', auth='public', website=True)
	def create_devis(self, **post):

		#Create contact first
		contact = request.env['res.partner'].sudo().create({
			'name': ' '.join([post.get('lastname'), post.get('firstname')]),
			'phone': post.get('phone'),
			'mobile': post.get('mobile'),
			'street': post.get('street'),
			'zip': post.get('zip'),
			'city': post.get('city'),
			'email': post.get('email'),
			'country_id' : int(post.get('country')),
			'm_gender': 'man' if str(post.get('gender')) == 'man' else 'woman',
			'm_years_old': int(post.get('yo')),
			'm_graft': True if str(post.get('grafted')) == "yes" else False,
		})

		#determine baldness degree
		baldness_environment = request.env['graft.baldness']
		domain = ['&', ('m_gender', '=', post.get('gender')), ('m_case', '=', post.get('case'))]
		baldness_id = baldness_environment.sudo().search(domain)
	

		

		#then create new operation with status
		operation_environment = request.env['graft.operation']
		operation = operation_environment.sudo().create({
			'm_patient': int(contact.id),
			'm_message': post.get('message'),
			'm_baldness': int(baldness_id),
			'm_donor_neck_filename' : str(post.get('donor_neck').filename) if post.get('donor_neck',False) else None,
			'm_donor_neck' : base64.b64encode(post.get('donor_neck').read()) if post.get('donor_neck',False) else None,
			'm_donor_side_filename' : str(post.get('m_donor_side').filename) if post.get('m_donor_side',False) else None,
			'm_donor_side' : base64.b64encode(post.get('donor_side').read()) if post.get('donor_side',False) else None,
			'm_treat_face_filename' : str(post.get('m_treat_face').filename) if post.get('m_treat_face',False) else None,
			'm_treat_face' : base64.b64encode(post.get('treat_face').read()) if post.get('treat_face',False) else None,
			'm_treat_side_filename' : str(post.get('m_treat_side').filename) if post.get('m_treat_side',False) else None,
			'm_treat_side' : base64.b64encode(post.get('treat_side').read()) if post.get('treat_side',False) else None,
			'm_treat_top_filename' : str(post.get('m_treat_top').filename) if post.get('m_treat_top',False) else None,
			'm_treat_top' : base64.b64encode(post.get('treat_top').read()) if post.get('treat_top',False) else None,
		})
		return http.request.redirect('/') #return http.request.redirect('http://www.lisboa-hair.com/')