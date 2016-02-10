from com.xebialabs.deployit.plugin.api.reflect import Type
from sets import Set

class RepositoryHelper(object):

    def __init__(self, repositoryService, metadataService):
        self.repositoryService = repositoryService
        self.metadataService = metadataService

    def create_or_update(self, ci_type, ci_id, ci_properties):
        ci = self.new_instance(ci_type,ci_id)
        for key, value in ci_properties.iteritems():
            print "set ci properties %s=%s" % (key,value)
            ci.setProperty(key,value)
        self.createOrUpdate(ci)


    def createOrUpdate(self, ci):
        if self.repositoryService.exists(ci.id):
            print "-- %s : updated" % ci
            return self.repositoryService.update(ci.id,ci)
        else:
            print "-- %s : created" % ci
            return self.repositoryService.create(ci.id,ci)

    def delete(self, ci_id):
        self.repositoryService.delete(ci_id)
        print "-- %s : deleted" % ci_id

    def new_instance(self, ci_type, ci_id):
        return self.metadataService.findDescriptor(Type.valueOf(ci_type)).newInstance(ci_id)

    def add_member(self,ci_id, ci_member_id):
        ci = self.repositoryService.read(ci_id)
        members = Set(ci.members)
        print "Add %s to %s" % (ci_member_id, members)
        members.add(self.repositoryService.read(ci_member_id))
        ci.members = members
        self.createOrUpdate(ci)

    def remove_member(self, ci_id, ci_member_id):
        if ci_id is None:
            print "Nothing to do...."
        else:
            ci = self.repositoryService.read(ci_id)
            print "Remove %s from %s" % (ci_member_id, ci.members)
            members = Set(ci.members)
            try:
                members.remove(self.repositoryService.read(ci_member_id))
                ci.members = members
                self.createOrUpdate(ci)
            except KeyError, e:
                print "%s member not found..skip" % str(e)




