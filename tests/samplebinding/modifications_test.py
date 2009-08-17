#!/usr/bin/python

'''Test cases for method modifications performed as described on typesystem. '''

import sys
import unittest

from sample import Modifications, Point

class ExtModifications(Modifications):
    def __init__(self):
        Modifications.__init__(self)

    def name(self):
        return 'ExtModifications'


class ModificationsTest(unittest.TestCase):
    '''Test cases for method modifications performed as described on typesystem. '''

    def setUp(self):
        self.mods = Modifications()

    def tearDown(self):
        del self.mods

    def testClassMembersAvailability(self):
        '''Test if Modified class really have the expected members.'''
        expected_members = set(['PolymorphicModFunc', 'PolymorphicNone',
                                'Polymorphic_ibiP', 'Polymorphic_ibib',
                                'Polymorphic_ibid', 'Polymorphic_ibii',
                                'calculateArea', 'doublePlus', 'increment',
                                'multiplyPointCoordsPlusValue', 'name',
                                'pointToPair', 'polymorphic', 'power',
                                'timesTen'])
        self.assert_(expected_members.issubset(dir(Modifications)))

    def testRenamedMethodAvailability(self):
        '''Test if Modification class really have renamed the 'className' virtual method to 'name'.'''
        self.assert_('className' not in dir(Modifications))
        self.assert_('name' in dir(Modifications))

    def testReimplementationOfRenamedVirtualMethod(self):
        '''Test if class inheriting from Modification class have the reimplementation of renamed virtual method called.'''
        em = ExtModifications()
        self.assertEqual(self.mods.name(), 'Modifications')
        self.assertEqual(em.name(), 'ExtModifications')

    def testRegularMethodRenaming(self):
        '''Test if Modifications::cppMultiply was correctly renamed to calculateArea.'''
        self.assert_('cppMultiply' not in dir(Modifications))
        self.assert_('calculateArea' in dir(Modifications))
        self.assertEqual(self.mods.calculateArea(3, 6), 3 * 6)

    def testRegularMethodRemoval(self):
        '''Test if 'Modifications::exclusiveCppStuff' was removed from Python bindings.'''
        self.assert_('exclusiveCppStuff' not in dir(Modifications))

    def testArgumentRemoval(self):
        '''Test if second argument of Modifications::doublePlus(int, int) was removed.'''
        self.assertRaises(TypeError, lambda : self.mods.doublePlus(3, 7))
        self.assertEqual(self.mods.doublePlus(7), 14)

    def testDefaultValueRemoval(self):
        '''Test if default value was removed from first argument of Modifications::increment(int).'''
        self.assertRaises(TypeError, self.mods.increment)
        self.assertEqual(self.mods.increment(7), 8)

    def testDefaultValueReplacement(self):
        '''Test if default values for both arguments of Modifications::power(int, int) were modified.'''
        # original default values: int power(int base = 1, int exponent = 0);
        self.assertNotEqual(self.mods.power(4), 1)
        # modified default values: int power(int base = 2, int exponent = 1);
        self.assertEqual(self.mods.power(), 2)
        self.assertEqual(self.mods.power(3), 3)
        self.assertEqual(self.mods.power(5, 3), 5**3)

    def testSetNewDefaultValue(self):
        '''Test if default value was correctly set to 10 for first argument of Modifications::timesTen(int).'''
        self.assertEqual(self.mods.timesTen(7), 70)
        self.assertEqual(self.mods.timesTen(), 100)

    def testArgumentRemovalAndReturnTypeModificationWithTypesystemTemplates1(self):
        '''Test modifications to method signature and return value using typesystem templates (case 1).'''
        result, ok = self.mods.pointToPair(Point(2, 5))
        self.assertEqual(type(ok), bool)
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(type(result[0]), float)
        self.assertEqual(type(result[1]), float)
        self.assertEqual(result[0], 2.0)
        self.assertEqual(result[1], 5.0)

    def testArgumentRemovalAndReturnTypeModificationWithTypesystemTemplates2(self):
        '''Test modifications to method signature and return value using typesystem templates (case 2).'''
        result, ok = self.mods.multiplyPointCoordsPlusValue(Point(2, 5), 4.1)
        self.assertEqual(type(ok), bool)
        self.assertEqual(type(result), float)
        self.assertEqual(result, 14.1)

    def testPolymorphicMethodModifications(self):
        '''Tests modifications to a polymorphic method'''
        # polymorphic(int, bool[removed], int, double)
        self.assertEqual(self.mods.polymorphic(1, 2, 3.1), Modifications.Polymorphic_ibid)
        # polymorphic(int, bool, int[removed,default=321], int)
        self.assertEqual(self.mods.polymorphic(1, True, 2), Modifications.Polymorphic_ibii)
        # the others weren't modified
        self.assertEqual(self.mods.polymorphic(1, True, 2, False), Modifications.Polymorphic_ibib)
        self.assertEqual(self.mods.polymorphic(1, False, 2, Point(3, 4)), Modifications.Polymorphic_ibiP)
        self.assertRaises(TypeError, lambda : self.mods.polymorphic(1, True, Point(2, 3), Point(4, 5)))
        self.assertEqual(self.mods.poly(1, True, Point(2, 3), Point(4, 5)), Modifications.Polymorphic_ibPP)

if __name__ == '__main__':
    unittest.main()

