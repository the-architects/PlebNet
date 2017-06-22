# -*- coding: utf-8 -*-
import ConfigParser
import codecs
import random

import unicodedata
from appdirs import user_config_dir
from cloudomate.util.config import UserOptions, os
from faker.factory import Factory


def _user_settings():
    settings = UserOptions()
    settings.read_settings()
    return settings


def status(provider):
    settings = _user_settings()
    return provider.get_status(settings)


def options(provider):
    return list(provider.start())


def purchase(provider, vps_option, wallet):
    settings = _user_settings()
    return provider.purchase(settings, vps_option, wallet)


def generate_config():
    config = UserOptions()
    filename = os.path.join(user_config_dir(), 'cloudomate.cfg')
    if os.path.exists(filename):
        print("cloudomate.cfg already present at %s" % filename)
        config.read_settings(filename=filename)
        return config
    locale = random.choice(['bg_BG', 'cs_CZ', 'de_DE', 'dk_DK', 'es_ES', 'et_EE', 'hr_HR', 'it_IT'])
    fake = Factory().create(locale)
    cp = ConfigParser.ConfigParser()
    _generate_address(cp, fake)
    _generate_server(cp, fake)
    _generate_user(cp, fake)
    _remove_unicode(cp)
    with codecs.open(filename, 'w', 'utf8') as config_file:
        cp.write(config_file)
    return cp


def _remove_unicode(cp):
    for section in cp.sections():
        for option in cp.options(section):
            item = cp.get(section, option)
            if isinstance(item, unicode):
                cp.set(section, option, unicodedata.normalize('NFKD', item).encode('ascii', 'ignore'))


def _generate_user(cp, fake):
    cp.add_section('User')
    firstname = fake.first_name()
    lastname = fake.last_name()
    cp.set('User', 'email', firstname + lastname + '@heijligers.me')
    cp.set('User', 'firstname', firstname)
    cp.set('User', 'lastname', lastname)
    cp.set('User', 'companyname', fake.company())
    cp.set('User', 'phonenumber', fake.numerify('##########'))
    cp.set('User', 'password', fake.password())


def _generate_address(cp, fake):
    cp.add_section('Address')
    cp.set('Address', 'address', fake.street_address())
    cp.set('Address', 'city', fake.city())
    cp.set('Address', 'state', fake.state())
    cp.set('Address', 'countrycode', fake.country_code())
    cp.set('Address', 'zipcode', fake.postcode())


def _generate_server(cp, fake):
    cp.add_section('Server')
    cp.set('Server', 'rootpw', fake.password())
    cp.set('Server', 'ns1', 'ns1')
    cp.set('Server', 'ns2', 'ns2')
    cp.set('Server', 'hostname', fake.word())
