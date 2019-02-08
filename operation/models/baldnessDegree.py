# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BaldnessDegree(models.Model):

	_name = 'graft.baldness'
	_rec_name = 'm_case'

	m_gender = fields.Selection([("man", "Homme"), ("woman", "Femme")], string="Sexe", default="man")
	m_image = fields.Binary(string="Image")
	m_case = fields.Selection([("1", "Cas 1"), ("2", "Cas 2"), ("3", "Cas 3"), ("4", "Cas 4")], string="Cas", default="1")