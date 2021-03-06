# -*- coding: utf-8 -*-
from board import Board
from member import Member


class Organization(object):

    """
    Class representing an organization
    """
    def __init__(self, client, organization_id,   name=''):
        self.client = client
        self.id = organization_id
        self.name = name

    @classmethod
    def from_json(cls, trello_client, json_obj):
        """
        Deserialize the board json object to a Organization object

        :trello_client: the trello client
        :json_obj: the board json object
        """
        organization = Organization(trello_client, json_obj['id'], name=json_obj['name'].encode('utf-8'))
        organization.description = json_obj.get('desc', '').encode('utf-8')
        # cannot close an organization
        # organization.closed = json_obj['closed']
        organization.url = json_obj['url']
        return organization

    def __repr__(self):
        return '<Organization %s>' % self.name

    def fetch(self):
        """Fetch all attributes for this organization"""
        json_obj = self.client.fetch_json('/organizations/' + self.id)
        self.name = json_obj['name']
        self.description = json_obj.get('desc', '')
        self.closed = json_obj['closed']
        self.url = json_obj['url']

    def all_boards(self):
        """Returns all boards on this organization"""
        return self.get_boards('all')

    def get_boards(self, list_filter):
        # error checking
        json_obj = self.client.fetch_json(
            '/organizations/' + self.id + '/boards',
            query_params={'lists': 'none', 'filter': list_filter})
        return [Board.from_json(organization=self, json_obj=obj) for obj in json_obj]

    def get_board(self, field_name):
        # error checking
        json_obj = self.client.fetch_json(
            '/organizations/' + self.id + '/boards',
            query_params={'filter': 'open', 'fields': field_name})
        return [Board.from_json(organization=self, json_obj=obj) for obj in json_obj]

    def get_members(self):
        json_obj = self.client.fetch_json(
            '/organizations/' + self.id + '/members',
            query_params={'filter': 'all'}
        )
        return [Member.from_json(trello_client=self.client, json_obj=obj) for obj in json_obj]
