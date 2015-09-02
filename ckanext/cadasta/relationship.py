import ckan.lib.base as base
import ckan.lib.helpers as helpers
from pylons import request
from ckan.controllers.package import PackageController
render = base.render
from ckan.lib.base import c
import model
from ckan.common import OrderedDict, _, json, request, c, g, response
from ckan.lib.search import SearchError

import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.maintain as maintain
import ckan.lib.i18n as i18n
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.accept as accept
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.datapreview as datapreview
import ckan.lib.plugins
import ckan.lib.uploader as uploader
import ckan.plugins as p
import ckan.lib.render
import cadasta_model
from datetime import datetime
from dateutil.parser import parse




NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
flatten_to_string_key = logic.flatten_to_string_key

lookup_package_plugin = ckan.lib.plugins.lookup_package_plugin


def get_surveys():
    surveys=[1,2,3,4,5,6,4,6]
    return surveys


def _encode_params(params):
    return [(k, v.encode('utf-8') if isinstance(v, basestring) else str(v))
            for k, v in params]


def url_with_params(url, params):
    params = _encode_params(params)
    return url + u'?' + urlencode(params)


def search_url(params, package_type=None):
    if not package_type or package_type == 'dataset':
        url = h.url_for(controller='package', action='search')
    else:
        url = h.url_for('{0}_search'.format(package_type))
    return url_with_params(url, params)




class Cadasta_Relationship_Controller(PackageController):


    def get_relationship_history(self, id, parcel_id):

        relationship_list = cadasta_model.get_relationship_history(parcel_id)

        if relationship_list:
            for relationship in relationship_list['features']:
                reformatted_date = parse(relationship['properties']['time_created'])
                reformatted_date = reformatted_date.strftime("%m/%d/%y")

                relationship['properties']['time_created'] = reformatted_date

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id' : parcel_id},
                                       package_type=package_type)

        return render('package/relationship_history.html',
                          extra_vars={'dataset_type': package_type, 'relationship_list':relationship_list})



    def read_relationship_details(self, id, parcel_id, relationship_id):

        relationship = cadasta_model.get_relationship_details(relationship_id)

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id': parcel_id, 'relationship_id': relationship_id},
                                       package_type=package_type)

        return render('package/relationship_details.html',
                          extra_vars={'dataset_type': package_type, 'relationship':relationship})



    def edit_relationship_details(self, id, parcel_id, relationship_id):

        relationship_details = cadasta_model.get_relationship_details(relationship_id)

        new_relationship = False

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id' : parcel_id, 'relationship_id': relationship_id},
                                       package_type=package_type)

        return render('package/edit_relationship_details.html',
                          extra_vars={'dataset_type': package_type, 'relationship_details': relationship_details, 'new_relationship': new_relationship})



    def new_relationship(self, id, parcel_id):

        new_relationship = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id': parcel_id},
                                       package_type=package_type)

        return render('package/edit_relationship_details.html',
                          extra_vars={'dataset_type': package_type, 'new_relationship':new_relationship })




    def show_relationship_map(self, id, parcel_id, relationship_id):

        relationship = cadasta_model.get_relationship_details(relationship_id)

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id': parcel_id, 'relationship_id': relationship_id},
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'id':id, 'parcel_id': parcel_id, 'relationship':relationship, 'relationship_id':relationship_id})



    def edit_relationship_map(self, id, parcel_id, relationship_id):

        relationship = cadasta_model.get_relationship_details(relationship_id)
        edit = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id': parcel_id, 'relationship_id': relationship_id},
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'id':id, 'parcel_id': parcel_id, 'relationship': relationship, 'relationship_id':relationship_id, 'edit':edit})




    def new_relationship_map(self, id, parcel_id):

        new = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id': parcel_id},
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'id':id, 'parcel_id': parcel_id, 'new': new})
