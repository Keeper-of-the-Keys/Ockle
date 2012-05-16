# PySNMP SMI module. Autogenerated from smidump -f python PYSNMP-MIB
# by libsmi2pysnmp-0.1.2 at Sat Nov 19 22:17:12 2011,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( Bits, Integer32, ModuleIdentity, MibIdentifier, TimeTicks, enterprises, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Integer32", "ModuleIdentity", "MibIdentifier", "TimeTicks", "enterprises")

# Objects

pysnmp = ModuleIdentity((1, 3, 6, 1, 4, 1, 20408)).setRevisions(("2005-05-14 00:00",))
if mibBuilder.loadTexts: pysnmp.setOrganization("pysnmp.sf.net")
if mibBuilder.loadTexts: pysnmp.setContactInfo("email: ilya@glas.net")
if mibBuilder.loadTexts: pysnmp.setDescription("Top-level infrastructure of the PySNMP project enterprise MIB tree")
pysnmpObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 1))
pysnmpExamples = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 2))
pysnmpEnumerations = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3))
pysnmpModuleIDs = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1))
pysnmpAgentOIDs = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 2))
pysnmpDomains = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 3))
pysnmpNotificationPrefix = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 4))
pysnmpNotifications = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 4, 0))
pysnmpNotificationObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 4, 1))
pysnmpConformance = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 5))
pysnmpCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 5, 1))
pysnmpGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 5, 2))
pysnmpExperimental = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 9999))

# Augmentions

# Exports

# Module identity
mibBuilder.exportSymbols("PYSNMP-MIB", PYSNMP_MODULE_ID=pysnmp)

# Objects
mibBuilder.exportSymbols("PYSNMP-MIB", pysnmp=pysnmp, pysnmpObjects=pysnmpObjects, pysnmpExamples=pysnmpExamples, pysnmpEnumerations=pysnmpEnumerations, pysnmpModuleIDs=pysnmpModuleIDs, pysnmpAgentOIDs=pysnmpAgentOIDs, pysnmpDomains=pysnmpDomains, pysnmpNotificationPrefix=pysnmpNotificationPrefix, pysnmpNotifications=pysnmpNotifications, pysnmpNotificationObjects=pysnmpNotificationObjects, pysnmpConformance=pysnmpConformance, pysnmpCompliances=pysnmpCompliances, pysnmpGroups=pysnmpGroups, pysnmpExperimental=pysnmpExperimental)

