import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def is_loaded(host, module):
    return host.run("kldstat -n %s.ko" % module).rc == 0


def in_loader_conf(host, module):
    return host.run("grep %s_load /boot/loader.conf" % module).rc == 0


def test_wsp_is_loaded_and_booted(host):
    assert in_loader_conf(host, "wsp")
    assert is_loaded(host, "wsp")


def test_wlan_acl_is_loaded_not_booted(host):
    assert not in_loader_conf(host, "wlan_acl")
    assert is_loaded(host, "wlan_acl")


def test_wlan_xauth_is_booted_not_loaded(host):
    assert in_loader_conf(host, "wlan_xauth")
    assert not is_loaded(host, "wlan_xauth")


def test_can_unload(host):
    assert not is_loaded(host, "s3")


def test_still_loaded(host):
    assert is_loaded(host, "fdescfs")
