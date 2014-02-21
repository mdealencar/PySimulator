'''
Copyright (C) 2011-2014 German Aerospace Center DLR
(Deutsches Zentrum fuer Luft- und Raumfahrt e.V.),
Institute of System Dynamics and Control
Copyright (C) 2014 ITI GmbH
All rights reserved.

This file is part of PySimulator.

PySimulator is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PySimulator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with PySimulator. If not, see www.gnu.org/licenses.
'''

'''
***************************
This Simulator plugin can load Modelica models (assumed SimulationX is installed),
simulate them by SimulationX and save the results.
***************************
'''

import csv
import pythoncom
import re
import os
import string
import time
import types
import _winreg as winreg
import win32com.client

import Plugins.SimulationResult.SimulationXCsv.SimulationXCsv as SimulationXCsv
import Plugins.Simulator.SimulatorBase

iconImage = 'simulatorSimulationX.ico'
modelExtension = ['mo', 'ism', 'isx']

# SimWindowStates
simWindowStateNormal = 0
simWindowStateMaximize = 1
simWindowStateMinimize = 2

# SimSpecialToolButtons
simSpecialToolButtonCurve = -1
SpecialToolButtonOptions = 0
SpecialToolButtonLast = 1
SpecialToolButtonNext = 2
SpecialToolButtonPrev = 3
SpecialToolButtonFirst = 4

# SimProperty
simIsHidden = 0
simIsSelected = 1
simNoStore = 2
simIsFinal = 3
simIsReplaceable = 4
simIsTypeAssign = 5
simIsBaseClass = 6
simIsToplevel = 7
simIsDisabled = 8
simIsDiscrete = 9
simIsDefaultDiscrete = 10
simIsInput = 11
simIsOutput = 12
simIsFlowVar = 13
simIsPartial = 14
simIsInner = 15
simIsOuter = 16
simIsModified = 17
simIsProtected = 18
simIsDynamic = 19
simValueMark = 20
simIsForCompat = 21
simIsAttribute = 22

# SimEntityClass
simEntity = 0
simNameSpace = 1
simParameter = 2
simRealParameter = 3
simIntParameter = 4
simBoolParameter = 5
simEnumeration = 6
simBoolean = 7
simString = 8
simVariable = 9
simRealVariable = 10
simIntVariable = 11
simBoolVariable = 12
simCurve = 13
simCurveSet = 14
simCurve2D = 15
simCurve3D = 16
simHystereseCurve = 17
simPin = 18
simConservPin = 19
simSignalInputPin = 20
simSignalOutputPin = 21
simPinRef = 22
simTypeAssign = 23
simTypedComponent = 24
simStateReference = 25
simFluidRef = 26
simFluid = 27
simFluidImpl = 28
simFluidMixture = 29
simFluidSet = 30
simAlias = 31
simSimObject = 32
simSimModel = 33
simSimBlock = 34
simFunction = 35
simConnection = 36
simSignalConnection = 37
simConservConnection = 38
simFluidConnection = 39
simActivityGroups = 40
simActivityGroup = 41
simDBGroup = 42
simLibrary = 43
simXSequence = 44
simYSequence = 45
simCurveMap = 46
simCurveAxis = 47
simCurveValues = 48
simGeneralParameter = 49
simGeneralCurve = 50
simSelEnum = 51
simModelicaPin = 52

# SimSolutionStates
simNoSolutionServer = 1
simReady = 2
simInitPrepare = 4
simRunning = 8
simStopped = 16
simFailed = 32
simContinuePrepare = 64
simBlocked = 128

# SimEntityKind
simType = 0
simComponent = 1
simModification = 2
simInstance = 3

# SimModelicaClass
simModClass = 0
simModRecord = 1
simModType = 2
simModConnector = 3
simModModel = 4
simModBlock = 5
simModPackage = 6
simModFunction = 7

# SimInitStates
simUninitialized = 0
simInitBase = 1
simInitAutomatic = 2
simInitManual = 3

# SimSpecialBlock
simSpecialBlockText = 0
simSpecialBlockImage = 1
simSpecialBlockNumber = 2
simSpecialBlockVBar = 3
simSpecialBlockHBar = 0
simSpecialBlockBulb = 4
simSpecialBlockMeter = 5
simSpecialBlockVSlider = 6
simSpecialBlockHSlider = 7
simSpecialBlockSwitch = 8

# SimStringFormat
SimFormatNone = 0
SimFormatDirectory = 1
SimFormatFileName = 2
SimFormatComputer = 3
SimFormatScript = 4
SimFormatExternalProgram = 5
SimFormatInternalModule = 6
SimFormatEvent = 7

# SimVariantsOutputFormat
SimVariantsOutputFormatText = 0
SimVariantsOutputFormatXML = 1
SimVariantsOutputFormatModel = 2

# SimCalculationMode
SimCalculationModeTransient = 0
SimCalculationModeEquilibration = 1

# SimTraceMsgType
SimTraceMsgTypeInfo = 0
SimTraceMsgTypeWarning = 1
SimTraceMsgTypeStop = 2
SimTraceMsgTypeQuestion = 3
SimTraceMsgTypeError = 4
SimTraceMsgTypeDebug = 5
SimTraceMsgTypeNone = 6

# SimTraceMsgLocation
SimTraceMsgCurrent = -1
SimTraceMsgSimulation = 0
SimTraceMsgLocationFile = 1

# SimTraceMsgLocation
SimTraceMsgCurrent = -1
SimTraceMsgSimulation = 0
SimTraceMsgLocationFile = 1

# SimViewInfoProperty
SimViewInfoPinPosition = 0
SimViewInfoPinDir = 1
SimViewInfoObjSize = 2
SimViewInfoObjImage = 3

# SimStatementKind
simAlgorithm = 0
simEquation = 1

# SimChildFilter
simGetTypes = 0
simGetNoTypes = 1
simGetBases = 2
simGetNoBases = 3
simGetAll = 4

# SimChildFilterFlags
simNoFilterFlags = 0
simResolveAliases = 1
simRecursive = 2

# SimTypeEditableFlags
simTypeNotEditable = 0
simTypeEditable = 1
simTypeDefaultEditable = 2

# SimCodeExportProject
simCodeExportProjectWithoutSolver = 0
simCodeExportProjectEmbeddedSolver = 1
simCodeExportProjectSFunction = 2

# SimCodeExportSaveOutputsApproach
simCodeExportSaveOutputsEqidistant = 0
simCodeExportSaveOutputsAll = 1
simCodeExportSaveOutputsAtleastwithdtProt = 2

# SimCurveMonotony
simDescendMon = -1
simNonMonoton = 0
simAscendMon = 1

# SimCurveInterpolation
simDefaultInterpol = 0
simLinearInterpol = 1
simStairsInterpol = 2
simSplineInterpol = 3
simHyperbolicApprox = 4
simArcApproc = 5

# SimFailureDataModes
simFailurePropagator = 0
simFailureNotRefined = 1
simFailureRefined = 2
simFailureBoth = 3
simFailureConnOr = 4
simFailureConnAnd = 5

def closeSimulatorPlugin():
	pass

def prepareSimulationList(fileName, name, config):
	pass

class Model(Plugins.Simulator.SimulatorBase.Model):

	def __init__(self, modelName, modelFileName, config):
		Plugins.Simulator.SimulatorBase.Model.__init__(self, modelName, modelFileName, 'SimulationX', config)

		sim = None
		try:
			if not config['Plugins']['SimulationX'].has_key('version'):
				config['Plugins']['SimulationX']['version'] = 'Iti.Simx36'
				config.write()
			dispatch = config['Plugins']['SimulationX']['version']

			pythoncom.CoInitialize()

			# A dummy object to get result properties:
			self.integrationResults = SimulationXCsv.Results('')
			self.integrationSettings.resultFileExtension = 'csvx'

			self._availableIntegrationAlgorithms = ['BDF', 'MEBDF', 'CVODE', 'FixedStep']

			self._IntegrationAlgorithmHasFixedStepSize = [False, False, False, True]
			self._IntegrationAlgorithmCanProvideStepSizeResults = [False, False, False, False]

			self.integrationSettings.algorithmName = self._availableIntegrationAlgorithms[0]
			self.simulationStopRequest = False

			# Open SimulationX
			sim = win32com.client.Dispatch(dispatch)

			# Show SimulationX window
			sim.Visible = True

			# Wait till SimulationX starts and loads Modelica
			if sim.InitState == simUninitialized:
				while sim.InitState != simInitBase:
					time.sleep(0.1)

			# SimulationX in non-interactive mode
			sim.Interactive = False

			if sim.InitState == simInitBase:
				sim.InitSimEnvironment() # Necessary when a script is used to start SimulationX

			self._doc = None

			if len(modelFileName) == 1:
				strMsg = 'PySimulator: Load model'

				split = string.rsplit(modelFileName[0], '.', 1)
				if len(split) > 1:
					suffix = split[1]
				else:
					suffix = ''

				if suffix in ['ism', 'isx']:
					# Try to load as file
					try:
						# Write tracing marker message to output window in SimulationX
						sim.Trace(SimTraceMsgLocationFile, SimTraceMsgTypeInfo, strMsg, '')
						self._doc = sim.Documents.Open(modelFileName[0])
					except win32com.client.pywintypes.com_error:
						self._doc = None
						print 'SimulationX: COM Error.'

				elif suffix == 'mo':
					# Try to load as library
					try:
						try:
							sim.LoadLibrary(modelFileName[0])
						except:
							pass
						# Write tracing marker message to output window in SimulationX
						sim.Trace(SimTraceMsgLocationFile, SimTraceMsgTypeInfo, strMsg, '')
						self._doc = sim.Documents.Open(modelName)
					except win32com.client.pywintypes.com_error:
						self._doc = None
						print 'SimulationX: COM Error.'

				if suffix in modelExtension:
					# Read complete tracing to string
					strTracing = sim.GetTraceMessages(SimTraceMsgLocationFile)
					# Find last occurrence of tracing marker message
					pos = strTracing.rfind(strMsg)
					if pos >= 0:
						strTracing = strTracing[pos + len(strMsg):].strip()
						if len(strTracing):
							print strTracing
							self._doc.Close(False)
							self._doc = None

				if not type(self._doc) is types.NoneType:
					self._marshalled_doc = pythoncom.CreateStreamOnHGlobal()
					pythoncom.CoMarshalInterface(self._marshalled_doc, pythoncom.IID_IDispatch, self._doc._oleobj_, pythoncom.MSHCTX_INPROC)
					self._marshalled_doc.Seek(0, pythoncom.STREAM_SEEK_SET)
				else:
					self._marshalled_doc = None
					print 'SimulationX: Load error.'

		except:
			print 'SimulationX: Error'

		finally:
			try:
				if not type(sim) is types.NoneType:
					# SimulationX in interactive mode
					sim.Interactive = True
			except:
				pass

	def __exit__(self, _type, _value, _traceback):
		pythoncom.CoReleaseMarshalData(self._marshalled_doc)
		pythoncom.CoUninitialize()

	def close(self):
		sim = None
		try:
			if not type(self._doc) is types.NoneType:
				sim = self._doc.Application
				sim.Interactive = False
				# Close model
				self._doc.Close(False)
				self._doc = None
				pythoncom.CoReleaseMarshalData(self._marshalled_doc)
		except win32com.client.pywintypes.com_error:
			print 'SimulationX: COM error.'
		finally:
			if not type(sim) is types.NoneType:
				sim.Interactive = True

		# Close the model
		Plugins.Simulator.SimulatorBase.Model.close(self)

	def _isNumeric(self, s):
		'''  Check if a string value can be successfully converted to a double value
		'''
		if not s:
			# Empty string
			return True
		else:
			try:
				float(s)
				return True
			except ValueError:
				return False
			except TypeError:
				return False

	def setVariableTree(self):
		''' Generate variable tree
		'''
		sim = None
		try:
			if not type(self._doc) is types.NoneType:
				sim = self._doc.Application
				sim.Interactive = False
				self._fillTree(self._doc, self._doc)
		except win32com.client.pywintypes.com_error:
			print 'SimulationX: COM error.'
		finally:
			if not type(sim) is types.NoneType:
				sim.Interactive = True

	def _fillTree(self, pObject, doc):
		''' Scan a SimulationX entity object for all child parameters and results
		'''
		for pBaseEntity in pObject.BaseEntities:
			self._fillTree(pBaseEntity, doc)

		for pChild in pObject.Children:
			childRelIdent = pChild.GetRelIdent(doc)
			if not pChild.Kind == simType:
				if not pChild.GetProperty(simIsBaseClass) and not pChild.GetProperty(simIsHidden) and not pChild.GetProperty(simIsProtected) and not pChild.GetProperty(simIsForCompat):
					childIsASimVariable = pChild.IsA(simVariable)
					if ((pChild.IsA(simParameter) or pChild.IsA(simGeneralParameter)) and not childIsASimVariable) or (pChild.GetProperty(simIsInput) and childIsASimVariable):
						# Parameter
						dim = pChild.Execute('GetDimension', [])[0]
						if dim == '':
							# Scalar dimension
							childTypeIdent = pChild.Type.Ident
							if not childTypeIdent == 'BuiltIn.BaseModel.ProtKind' and not childTypeIdent == 'StateSelect' and self._isNumeric(pChild.Value):
								childRelIdent = pChild.GetRelIdent(doc)
								if (not pChild.Parent == doc and not pObject.Name.find('_base') == 0) or (not childRelIdent == 'iSim' and not childRelIdent == 'tStart' and not childRelIdent == 'tStop'):
									childValue = pChild.Value
									childValueEdit = True
									childUnit = pChild.Unit
									if childUnit == '-':
										childUnit = None
									childVariability = 'fixed'
									childVariableAttr = ''
									childComment = pChild.comment
									if childComment != '':
										childVariableAttr += 'Description:' + chr(9) + childComment + '\n'
									childVariableAttr += 'Causality:' + chr(9) + 'parameter' + '\n'
									childVariableAttr += 'Variability:' + chr(9) + childVariability # + '\n'
									self.variableTree.variable[childRelIdent] = Plugins.Simulator.SimulatorBase.TreeVariable(self.structureVariableName(childRelIdent), childValue, childValueEdit, childUnit, childVariability, childVariableAttr)
						elif self._isNumeric(dim):
							# Fixed vector dimension
							childTypeIdent = pChild.Type.Ident
							if not childTypeIdent == 'BuiltIn.BaseModel.ProtKind' and not childTypeIdent == 'StateSelect':
								childRelIdent = pChild.GetRelIdent(doc)
								if (not pChild.Parent == doc and not pObject.Name.find('_base') == 0) or (not childRelIdent == 'iSim' and not childRelIdent == 'tStart' and not childRelIdent == 'tStop'):
									dim = int(dim)
									childValue = pChild.Value
									childValue = re.sub('[\{\}\[\] ]', '', childValue)
									childValue = childValue.replace(';', ',')
									childValueList = childValue.split(',')
									if len(childValueList) == dim:
										childValueEdit = True
										childUnit = pChild.Unit
										if childUnit == '-':
											childUnit = None
										childVariability = 'fixed'
										childVariableAttr = ''
										childComment = pChild.Comment
										if childComment != '':
											childVariableAttr += 'Description:' + chr(9) + childComment + '\n'
										childVariableAttr += 'Causality:' + chr(9) + 'parameter' + '\n'
										childVariableAttr += 'Variability:' + chr(9) + childVariability # + '\n'
										for i in range(1, dim + 1):
											if self._isNumeric(childValueList[i - 1]):
												self.variableTree.variable[childRelIdent + '[' + str(i) + ']'] = Plugins.Simulator.SimulatorBase.TreeVariable(self.structureVariableName(childRelIdent + '[' + str(i) + ']'), childValueList[i - 1], childValueEdit, childUnit, childVariability, childVariableAttr)
					elif childIsASimVariable:
						# Result
						dim = pChild.Execute('GetDimension', [])[0]
						if dim == '':
							# Scalar dimension
							childRelIdent = pChild.GetRelIdent(doc)
							if (not pChild.Parent == doc and not pObject.Name.find('_base') == 0) or (not childRelIdent == 't' and not childRelIdent == 'dt' and not childRelIdent == 'solverInfo' and not childRelIdent == 'lambdaHomotopy'):
								childValue = None
								childValueEdit = False
								childUnit = pChild.Unit
								if childUnit == '-':
									childUnit = None
								if (pChild.GetProperty(simIsDiscrete)):
									childVariability = 'discrete'
								else:
									childVariability = 'continuous'
								childVariableAttr = ''
								childComment = pChild.Comment
								if childComment != '' :
									childVariableAttr += 'Description:' + chr(9) + childComment + '\n'
								childVariableAttr += 'Causality:' + chr(9) + 'state' + '\n'
								childVariableAttr += 'Variability:' + chr(9) + childVariability # + '\n'
								self.variableTree.variable[childRelIdent] = Plugins.Simulator.SimulatorBase.TreeVariable(self.structureVariableName(childRelIdent), childValue, childValueEdit, childUnit, childVariability, childVariableAttr)
						elif self._isNumeric(dim):
							# Fixed vector dimension
							childRelIdent = pChild.GetRelIdent(doc)
							if (not pChild.Parent == doc and not pObject.Name.find('_base') == 0) or (not childRelIdent == 't' and not childRelIdent == 'dt' and not childRelIdent == 'solverInfo' and not childRelIdent == 'lambdaHomotopy'):
								dim = int(dim)
								childValue = None
								childValueEdit = False
								childUnit = pChild.Unit
								if childUnit == '-':
									childUnit = None
								if (pChild.GetProperty(simIsDiscrete)):
									childVariability = 'discrete'
								else:
									childVariability = 'continuous'
								childVariableAttr = ''
								childComment = pChild.Comment
								if childComment != '':
									childVariableAttr += 'Description:' + chr(9) + childComment + '\n'
								childVariableAttr += 'Causality:' + chr(9) + 'state' + '\n'
								childVariableAttr += 'Variability:' + chr(9) + childVariability # + '\n'
								for i in range(1, dim + 1):
									self.variableTree.variable[childRelIdent + '[' + str(i) + ']'] = Plugins.Simulator.SimulatorBase.TreeVariable(self.structureVariableName(childRelIdent + '[' + str(i) + ']'), childValue, childValueEdit, childUnit, childVariability, childVariableAttr)
				childIsOuter = pChild.GetProperty(simIsOuter)
				if not childIsOuter or (childIsOuter and pChild.GetProperty(simIsInner)):
					childEntityClass = pChild.Class
					if childEntityClass == simSimObject or childEntityClass == simSimBlock or childEntityClass == simConservConnection or childEntityClass == simFluidConnection:
						self._fillTree(pChild, doc)

	def getReachedSimulationTime(self):
		''' Read the current simulation time during a simulation
		'''
		sim = None
		rTime = None
		try:
			if not type(self._doc) is types.NoneType:
				sim = self._doc.Application
				sim.Interactive = False
				if self._doc.SolutionState > simReady:
					rTime = self._doc.Lookup('t').LastValue
		except:
			rTime = None
		finally:
			if not type(sim) is types.NoneType:
				sim.Interactive = True

		return rTime

	def simulate(self):
		''' Run a simulation of a Modelica/SimulationX model
		'''
		sim = None
		try:
			pythoncom.CoInitialize()
			doc = win32com.client.Dispatch(pythoncom.CoUnmarshalInterface(self._marshalled_doc, pythoncom.IID_IDispatch))
			self._marshalled_doc.Seek(0, pythoncom.STREAM_SEEK_SET)
			if not type(doc) is types.NoneType:
				sim = doc.Application
				sim.Interactive = False
				self._simulate_sync(doc)
		except win32com.client.pywintypes.com_error:
			print 'SimulationX: COM error.'
			raise(Plugins.Simulator.SimulatorBase.Stopping)
		except:
			raise(Plugins.Simulator.SimulatorBase.Stopping)
		finally:
			if not type(sim) is types.NoneType:
				sim.Interactive = True
			pythoncom.CoUninitialize()

	def _simulate_sync(self, doc):
		simulation = self.integrationSettings

		# Integration settings
		doc.Lookup('tStart').Value = simulation.startTime
		doc.Lookup('tStop').Value = simulation.stopTime
		doc.Lookup('relTol').Value = simulation.errorToleranceRel
		if simulation.errorToleranceAbs is None:
			doc.Lookup('absTol').Value = simulation.errorToleranceRel
		else:
			doc.Lookup('absTol').Value = simulation.errorToleranceAbs

		ialg = self._availableIntegrationAlgorithms.index(simulation.algorithmName)
		if self._IntegrationAlgorithmHasFixedStepSize[ialg]:
			doc.Lookup('dtMin').Value = simulation.fixedStepSize
		else:
			doc.Lookup('dtMin').Value = 1e-008
		if simulation.gridPointsMode == 'NumberOf':
			if simulation.gridPoints > 1:
				gridWidth = (simulation.stopTime - simulation.startTime)/(simulation.gridPoints - 1)
			else:
				gridWidth = (simulation.stopTime - simulation.startTime)/500
		elif simulation.gridPointsMode == 'Width':
			gridWidth = simulation.gridWidth
		doc.Lookup('dtProtMin').Value = gridWidth
		doc.Lookup('protKind').Value = 0 # = 'BaseModel.ProtKind.EquidistantTimeSteps'
		doc.SolverByName = simulation.algorithmName

		for name, newValue in self.changedStartValue.iteritems():
			i = name.find('[')
			if i >= 0 and name.endswith(']'):
				value = doc.Parameters(name[0:i]).Value
				n = name[i:]
				n = re.sub('[\[\]]', '', n)
				if self._isNumeric(n):
					n = int(n)
					value = re.sub('[\{\}\[\] ]', '', value)
					value = value.replace(';', ',')
					valueList = value.split(',')
					valueList[n - 1] = newValue
					doc.Parameters(name[0:i]).Value = '{' + ','.join(valueList) + '}'
			else:
				doc.Parameters(name).Value = newValue

		# Log all variables
		for name in self.variableTree.variable.iteritems():
			pChild = doc.Lookup(name[0])
			if pChild.IsA(simVariable) and not pChild.GetProperty(simIsInput):
				try:
					pChild.Protocol = True
				except:
					try:
						pChild.Parent.Results(pChild.Name).Protocol = True
					except:
						pass

		# Start simulation
		doc.Reset()
		time.sleep(0.01)
		doc.Start()

		# Wait till simulation is finished
		while doc.SolutionState < simStopped:
			if self.simulationStopRequest:
				doc.Stop()
				self.simulationStopRequest = False
				raise(Plugins.Simulator.SimulatorBase.Stopping)
			time.sleep(0.1)

		# Integration is finished
		# Log all parameters
		paramName = list()
		paramUnit = list()
		paramValue = list()
		for name in self.variableTree.variable.iteritems():
			pChild = doc.Lookup(name[0])
			childIsASimVariable = pChild.IsA(simVariable)
			if ((pChild.IsA(simParameter) or pChild.IsA(simGeneralParameter)) and not childIsASimVariable) or (pChild.GetProperty(simIsInput) and childIsASimVariable):
				childRelIdent = pChild.GetRelIdent(doc)
				childUnit = pChild.Unit
				childValue = pChild.Value
				dim = pChild.Execute('GetDimension', [])[0]
				if dim == '':
					# Scalar dimension
					paramName.append(childRelIdent)
					paramUnit.append(childUnit)
					if childValue == '':
						childValue = 0
					paramValue.append(childValue)
				elif self._isNumeric(dim):
					# Fixed vector dimension
					dim = int(dim)
					childValue = re.sub('[\{\}\[\] ]', '', childValue)
					childValue = childValue.replace(';', ',')
					childValueList = childValue.split(',')
					if len(childValueList) == dim:
						for i in range(1, dim + 1):
							if self._isNumeric(childValueList[i - 1]):
								paramName.append(childRelIdent + '[' + str(i) + ']')
								paramUnit.append(childUnit)
								childValue = childValueList[i - 1]
								if childValue == '':
									childValue = 0
								paramValue.append(childValue)

		if doc.SolutionState == simStopped:
			# Save results in CSV file
			resultFileName = os.path.abspath(simulation.resultFileName).replace('\\', '/')
			ver = self.config['Plugins']['SimulationX']['version']
			if ver == 'Iti.Simx36':
				ver = '3.6'
			elif ver == 'Iti.Simx37':
				ver = '3.7'
			else:
				ver = '3.5'
			key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\ITI GmbH\SimulationX ' + ver + r'\DataFilter', 0, winreg.KEY_ALL_ACCESS)
			frt = winreg.QueryValueEx(key, 'Format')
			dec = winreg.QueryValueEx(key, 'Dec')
			sep = winreg.QueryValueEx(key, 'Separator')
			adT = winreg.QueryValueEx(key, 'AddTableName')
			adN = winreg.QueryValueEx(key, 'AddColumnNames')
			adU = winreg.QueryValueEx(key, 'AddColumnUnits')
			winreg.SetValueEx(key, 'Format', 0, winreg.REG_SZ, '%.17lg')
			winreg.SetValueEx(key, 'Dec', 0, winreg.REG_SZ, '.')
			winreg.SetValueEx(key, 'Separator', 0, winreg.REG_SZ, ';')
			winreg.SetValueEx(key, 'AddTableName', 0, winreg.REG_DWORD, 0)
			winreg.SetValueEx(key, 'AddColumnNames', 0, winreg.REG_DWORD, 1)
			winreg.SetValueEx(key, 'AddColumnUnits', 0, winreg.REG_DWORD, 1)
			winreg.FlushKey(key)
			doc.StoreAllResultsAsText(resultFileName)
			winreg.SetValueEx(key, 'Format', 0, winreg.REG_SZ, frt[0])
			winreg.SetValueEx(key, 'Dec', 0, winreg.REG_SZ, dec[0])
			winreg.SetValueEx(key, 'Separator', 0, winreg.REG_SZ, sep[0])
			winreg.SetValueEx(key, 'AddTableName', 0, winreg.REG_DWORD, adT[0])
			winreg.SetValueEx(key, 'AddColumnNames', 0, winreg.REG_DWORD, adN[0])
			winreg.SetValueEx(key, 'AddColumnUnits', 0, winreg.REG_DWORD, adU[0])
			winreg.CloseKey(key)

			# Save parameters in CSV file
			if len(paramName) > 0:
				with open(resultFileName + 'p', 'wb') as csvfile:
					csvwriter = csv.writer(csvfile, delimiter = ';')
					csvwriter.writerow(paramName)
					csvwriter.writerow(paramUnit)
					csvwriter.writerow(paramValue)

			self.integrationStatistics.reachedTime = simulation.stopTime
			self.integrationStatistics.nGridPoints = len(doc.Lookup('t').ProtValues)
		elif doc.SolutionState == simFailed:
			print('SimulationX: Simulation error.')

	def getAvailableIntegrationAlgorithms(self):
		''' Returns a list of strings with available integration algorithms
		'''
		return self._availableIntegrationAlgorithms

	def getIntegrationAlgorithmHasFixedStepSize(self, algorithmName):
		''' Returns True or False dependent on the fact,
			if the integration algorithm given by the string algorithmName
			has a fixed step size or not (if not it has a variable step size).
		'''
		return self._IntegrationAlgorithmHasFixedStepSize[self._availableIntegrationAlgorithms.index(algorithmName)]

	def getIntegrationAlgorithmCanProvideStepSizeResults(self, algorithmName):
		''' Returns True or False dependent on the fact,
			if the integration algorithm given by the string algorithmName
			can provide result points at every integration step.
		'''
		return self._IntegrationAlgorithmCanProvideStepSizeResults[self._availableIntegrationAlgorithms.index(algorithmName)]
