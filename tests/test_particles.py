import unittest

from utilities import particles
from utilities import structure


class Test_get_quark_composition(unittest.TestCase):
    def test_baryons(self):
        self.assertEqual(
            particles.Particle.get_quark_composition(
                "1.0/sqrt(2.0) * [u^{a} (C\gamma_{5}) d^{b}] (I) u^{c}"
            ),
            ["u", "u", "d"],
        )
        self.assertEqual(
            particles.Particle.get_quark_composition(
                "1.0/sqrt(2.0) * [u^{a} (C\gamma_{5}) s^{b}] (I) u^{c}"
            ),
            ["u", "u", "s"],
        )
        self.assertEqual(
            particles.Particle.get_quark_composition(
                "1.0/sqrt(2.0) * [d^{a} (C\gamma_{5}) s^{b}] (I) d^{c}"
            ),
            ["d", "d", "s"],
        )
        self.assertEqual(
            particles.Particle.get_quark_composition(
                "1.0/sqrt(2.0) * [d^{a} (C\gamma_{5}) s^{b}] (I) s^{c}"
            ),
            ["d", "s", "s"],
        )


class Test_get_particle_charge(unittest.TestCase):
    uds = structure.Structure(["u", "d", "s"])
    nlds = structure.Structure(["nl", "d", "s"])
    dds = structure.Structure(["d", "d", "s"])

    def test_baryon(self):
        self.assertEqual(particles.get_particle_charge("proton_1", self.uds), 1)
        self.assertEqual(particles.get_particle_charge("proton_1", self.nlds), -1 / 3)
        self.assertEqual(particles.get_particle_charge("proton_1", self.dds), -1)
        self.assertEqual(particles.get_particle_charge("neutron_1", self.uds), 0)
        self.assertEqual(particles.get_particle_charge("neutron_1", self.nlds), -2 / 3)
        self.assertEqual(particles.get_particle_charge("neutron_1", self.dds), -1)
        self.assertEqual(particles.get_particle_charge("cascade0_1", self.uds), 0)
        self.assertEqual(particles.get_particle_charge("cascade0_1", self.nlds), -2 / 3)
        self.assertEqual(particles.get_particle_charge("cascade0_1", self.dds), -1)

    def test_baryon_bar(self):
        self.assertEqual(particles.get_particle_charge("proton_1bar", self.uds), -1)
        self.assertEqual(particles.get_particle_charge("proton_1bar", self.nlds), 1 / 3)
        self.assertEqual(particles.get_particle_charge("proton_1bar", self.dds), 1)
        self.assertEqual(particles.get_particle_charge("neutron_1bar", self.uds), 0)
        self.assertEqual(
            particles.get_particle_charge("neutron_1bar", self.nlds), 2 / 3
        )
        self.assertEqual(particles.get_particle_charge("neutron_1bar", self.dds), 1)
        self.assertEqual(particles.get_particle_charge("cascade0_1bar", self.uds), 0)
        self.assertEqual(
            particles.get_particle_charge("cascade0_1bar", self.nlds), 2 / 3
        )
        self.assertEqual(particles.get_particle_charge("cascade0_1bar", self.dds), 1)

    def test_meson(self):
        self.assertEqual(particles.get_particle_charge("pip", self.uds), 1)
        self.assertEqual(particles.get_particle_charge("pip", self.dds), 0)
        self.assertEqual(particles.get_particle_charge("pip", self.nlds), 1 / 3)
        self.assertEqual(particles.get_particle_charge("kaonp", self.uds), 1)
        self.assertEqual(particles.get_particle_charge("kaonp", self.dds), 0)
        self.assertEqual(particles.get_particle_charge("kaonp", self.nlds), 1 / 3)

    def test_meson_bar(self):
        self.assertEqual(particles.get_particle_charge("pipbar", self.uds), -1)
        self.assertEqual(particles.get_particle_charge("pipbar", self.dds), 0)
        self.assertEqual(particles.get_particle_charge("pipbar", self.nlds), -1 / 3)
        self.assertEqual(particles.get_particle_charge("kaonpbar", self.uds), -1)
        self.assertEqual(particles.get_particle_charge("kaonpbar", self.dds), 0)
        self.assertEqual(particles.get_particle_charge("kaonpbar", self.nlds), -1 / 3)
