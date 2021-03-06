# -*- coding: utf-8 -*-


class Member(object):
    """
    Class representing a Trello member.
    """

    def __init__(self, client, member_id, full_name=''):
        self.client = client
        self.id = member_id
        self.full_name = full_name

    def __repr__(self):
        return '<Member %s>' % self.id

    def fetch(self):
        """Fetch all attributes for this member"""
        json_obj = self.client.fetch_json(
            '/members/' + self.id,
            query_params={'badges': False})
        self.status = json_obj['status']
        self.id = json_obj.get('id', '')
        self.bio = json_obj.get('bio', '')
        self.url = json_obj.get('url', '')
        self.username = json_obj['username']
        self.full_name = json_obj['fullName']
        self.initials = json_obj['initials']
        self.avatar_has = json_obj['avatarHash']
        return self

    def fetch_comments(self):
        comments = []
        if self.badges['comments'] > 0:
            comments = self.client.fetch_json(
                '/members/' + self.id + '/actions',
                query_params={'filter': 'commentCard'})
        return comments

    @property
    def avatar_url(self, size='large'):
        """
        Return url for member avatar
        
        :param size: can be 'small' (30x30) or 'large' (170x170)
        """
        size = 30 if size is 'small' else 170
        url= "https://trello-avatars.s3.amazonaws.com/{avatar_id}/{size}".format(
                avatar_id=self.id,
                size=size)
        return url

    @classmethod
    def from_json(cls, trello_client, json_obj):
        """
        Deserialize the organization json object to a member object

        :trello_client: the trello client
        :json_obj: the member json object
        """

        member = Member(trello_client, json_obj['id'], full_name=json_obj['fullName'].encode('utf-8'))
        member.username = json_obj.get('username', '').encode('utf-8')
        member.initials = json_obj.get('initials', '').encode('utf-8')
        # cannot close an organization
        # organization.closed = json_obj['closed']
        return member
