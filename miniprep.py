import opentrons_functions as of
import sys

print("THIS PROTOCOL USES THE OT2")

# https://doi.org/10.1093/nar/27.24.e37
## =============================================
## SETUP THE OT-2 DECK
## =============================================
locations = {
        '1':'Output Plate',
        '2':'',
        '3':'',
        '4':'300uL Tips',
        '5':'DeepWell_Cells',
        '6':'H2O',
        '7':'300uL Tips',
        '8':'Dilutant',
        '9':'Lysis_buffer',
        '10':'',
        '11':''
        }

of.show_deck_OT2(locations)

sys.exit()
tiprack = labware.load('tiprack-200ul', '4')
tiprack2 = labware.load('tiprack-200ul', '7')

deep_plate = labware.load('96-deep-well', '5')
output_plate = labware.load('96-well', '1')

H2O_trough = labware.load('trough-12row','6')
lysis_trough = labware.load('trough-12row','9')
dilution_trough = labware.load('trough-12row','8')

pipette = instruments.P300_Multi(mount='left', tip_racks=[tiprack, tiprack2])
pipette.set_pick_up_current(0.8)

## ========================
## Add 25ul of H2O to cells
## ========================

print("Running plate on {}")
#robot.home()
#p200_tipracks = [containers.load('tiprack-200ul', locations['tiprack-200']),
        #]
