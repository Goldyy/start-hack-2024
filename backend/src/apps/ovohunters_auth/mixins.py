class KeycloakServicesMixins:
    @property
    def group_name(self):
        return self.request.POST.get('groupName')

    @property
    def attributes(self):
        return self.request.POST.get('attributes')

    @property
    def address(self):
        return self.request.POST.get('attributes')['address']


