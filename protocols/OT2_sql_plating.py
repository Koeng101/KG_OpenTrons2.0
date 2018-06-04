from opentrons import robot, labware, instruments

def OT2_plate(rxns, per_plate=24):
    
    ### Parameter setup ###
    num_plates = ((rxns - 1) // per_plate) + 1
    if num_plates > 4: raise ValueError("Too many plates needed. Max 96 reactions.")

    transformation_rows = rxns // 8 + (rxns % 8 > 0)

    num_dilutions = 4

    ### Bot setup ###
    robot.home()
    robot.connect()
    tiprack = labware.load('tiprack-10ul', '11')
    transformation = labware.load('96-flat', '10')
    trash_liquid = labware.load('trough-1row-25ml', '9')
    wash_liquid = labware.load('trough-1row-25ml', '8')
    LB = labware.load('trough-1row-25ml', '7')
    agar_plates = []
    for plate in range(num_plates):
        placement = str(6 - plate)
        agar_plates.append(labware.load('96-deep-well', placement))
    pipette = instruments.P10_Multi(mount='right', tip_racks=tiprack)

    ### Pickup tips ###
    pipette.set_pick_up_current(0.8)
    pipette.pick_up_tip(tiprack)

    ###
    def wash_tip(wash_liquid=wash_liquid):
        pipette.move_to(wash_liquid.bottom())
        pipette.mix(4)
        pipette.move_to(wash_liquid.bottom(50))
        pipette.blow_out()

    def ditch_liquid(trash_liquid=trash_liquid):
        pipette.move_to(trash_liquid)
        pipette.dispense(trash_liquid)
        pipette.mix(4)
        pipette.move_to(trash_liquid.bottom(50))
        pipette.blow_out()

    def dilute_well(transformation_row, LB=LB, dilution_vol=9):
        pipette.transfer(dilution_vol, LB, transformation_row, new_tip='never')
        pipette.mix(2)

    def plate(transformation_row, agar_plate_row, plate_vol=7.5, dilution_vol=9):
        pipette.aspirate(dilution_vol, transformation_row)
        pipette.move_to(agar_plate_row.bottom(20))
        pipette.blow_out()
        pipette.move_to(agar_plate_row.bottom(-3))
        pipette.move_to(agar_plate_row.bottom(20))

    def plate_to_wash(transformation_row, agar_plate_row, LB=LB, trash_liquid=trash_liquid, wash_liquid=wash_liquid):
        dilute_well(transformation_row, LB)
        plate(transformation_row, agar_plate_row)
        ditch_liquid(trash_liquid)
        wash_tip(wash_liquid)

    def plate_row(transformation_row, agar_plate, LB=LB, trash_liquid=trash_liquid, wash_liquid=wash_liquid, num_dilutions=4, counter=0):
        # Counter has 3 values: [0,1,2]. Thesse are how row_plate can skip sections that are done.
        counter *= 4
        for agar_well in range(num_dilutions):
            well_label = "A" + str((agar_well + 1) + counter)
            print("Plating transformation row {} to agar plate {} well {}".format(transformation_row, agar_plate, well_label))
            plate_to_wash(transformation_row, agar_plate.wells(well_label), LB, trash_liquid, wash_liquid)

    ### For loop setup
    counter = 0
    agar_counter = 0
    agar_plate = agar_plates[agar_counter]

    ### Plate procedure
    for rows in range(transformation_rows):
        transformation_row = "A" + str(rows + 1)
        print("Plating row",transformation_row)
        if (counter + 1) % num_dilutions == 0:
            counter = 0
            agar_counter += 1
            agar_plate = agar_plates[agar_counter]
        plate_row(transformation.wells(transformation_row), agar_plate, counter=counter)
        counter += 1

    ### Drop tips
    pipette.drop_tip()

OT2_plate(48)
