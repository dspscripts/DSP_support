import numpy as np
from typing import List, Optional, Dict
import argparse

building_speed_dict = {
    "matrix lab": 1.0,
    "assembler3": 1.5,
    "assembler2": 1.0,
    "assembler1": 0.75,
    "smelter2": 2.0,
    "smelter1": 1,
    "chemical facility": 1.0,
    "oil refinery": 1.0,
    "particle collider": 1.0,
    "fractionator": 1.0,
    "ray receiver": 1.0,
}

proliferate_dict = {
    0: 1.0,
    1: 1.125,
    2: 1.2,
    3: 1.25,
}


item_dict = {
    "antimatter": {
        "building": "particle collider",
        "ingredients": ["2 critical_photon"],
        "craft_speed": 2,
        "output": 2,
    },
    "blue_cube": {
        "building": "matrix lab",
        "ingredients": ["1 magnetic_coil", "1 circuit_board"],
        "craft_speed": 3,
        "output": 1,
    },
    "carbon_nanotube": {
        "building": "chemical facility",
        "ingredients": ["2 spinoform"],
        "craft_speed": 4,
        "output": 2,
    },
    "casimir_crystal": {
        "building": "assembler",
        "ingredients": ["4 optical_crystal", "2 graphene", "12 hydrogen"],
        "craft_speed": 8,
        "output": 1,
    },
    "circuit_board": {
        "building": "assembler",
        "ingredients": ["2 iron_ingot", "1 copper_ingot"],
        "craft_speed": 1,
        "output": 2,
    },
    "critical_photon": {
        "building": "ray receiver",  # assume graviton lens are used
        "ingredients": ["240 swarm_sphere_MW"],
        "craft_speed": 60,
        "output": 12,
    },
    "crystal_silicon": {
        "building": "assembler",
        "ingredients": ["1 fractal_silicon"],
        "craft_speed": 1.5,
        "output": 2,
    },
    "deuterium": {
        "building": "fractionator",  # assumes an always fully stacked (4) mk3 belt (1% of 120 hydrogen/seconds)
        "ingredients": [
            "12 hydrogen_frac"
        ],  # we first need 120/sec, but once you get those, you actually just need to replenish 1.2/s
        "craft_speed": 10,  # just to keep the number of ingredients/output integers
        "output": 12,
    },
    "diamond": {
        "building": "smelter",
        "ingredients": ["1 kimberlite_ore"],
        "craft_speed": 1.5,
        "output": 2,
    },
    "electric_motor": {
        "building": "assembler",
        "ingredients": ["2 iron_ingot", "1 gear", "1 magnetic_coil"],
        "craft_speed": 2,
        "output": 1,
    },
    "gear": {
        "building": "assembler",
        "ingredients": ["1 iron_ingot"],
        "craft_speed": 1,
        "output": 1,
    },
    "graphene": {
        "building": "chemical facility",
        "ingredients": ["2 fire_ice"],
        "craft_speed": 2,
        "output": 2,
    },
    "graviton_lens": {
        "building": "assembler",
        "ingredients": ["4 diamond", "1 strange_matter"],
        "craft_speed": 6,
        "output": 1,
    },
    "green_cube": {
        "building": "matrix lab",
        "ingredients": ["1 graviton_lens", "1 quantum_chip"],
        "craft_speed": 24,
        "output": 2,
    },
    "magnetic_coil": {
        "building": "assembler",
        "ingredients": ["2 magnet", "1 copper_ingot"],
        "craft_speed": 1,
        "output": 2,
    },
    "microcrystaline_component": {
        "building": "assembler",
        "ingredients": ["2 silicon_ingot", "1 copper_ingot"],
        "craft_speed": 2,
        "output": 1,
    },
    "particle_broadband": {
        "building": "assembler",
        "ingredients": ["2 carbon_nanotube", "2 crystal_silicon", "1 plastic"],
        "craft_speed": 8,
        "output": 1,
    },
    "particle_container": {
        "building": "assembler",
        "ingredients": ["2 graphene", "2 iron_ingot", "2 turbine"],
        "craft_speed": 4,
        "output": 1,
    },
    "plane_filter": {
        "building": "assembler",
        "ingredients": ["1 casimir_crystal", "2 titanium_glass"],
        "craft_speed": 12,
        "output": 1,
    },
    "plastic": {
        "building": "chemical facility",
        "ingredients": ["2 refined_oil", "1 energetic_graphite"],
        "craft_speed": 3,
        "output": 1,
    },
    "processor": {
        "building": "assembler",
        "ingredients": ["2 circuit_board", "2 microcrystaline_component"],
        "craft_speed": 3,
        "output": 1,
    },
    "purple_cube": {
        "building": "matrix lab",
        "ingredients": ["2 processor", "1 particle_broadband"],
        "craft_speed": 10,
        "output": 1,
    },
    "quantum_chip": {
        "building": "assembler",
        "ingredients": ["2 processor", "2 plane_filter"],
        "craft_speed": 6,
        "output": 1,
    },
    "red_cube": {
        "building": "matrix lab",
        "ingredients": ["2 energetic_graphite", "2 hydrogen"],
        "craft_speed": 6,
        "output": 1,
    },
    "refined_oil": {
        "building": "oil refinery",
        "ingredients": ["2 crude_oil"],
        "craft_speed": 4,
        "output": 2,
    },
    "strange_matter": {
        "building": "particle collider",
        "ingredients": ["2 particle_container", "2 iron_ingot", "10 deuterium"],
        "craft_speed": 8,
        "output": 1,
    },
    "titanium_crystal": {
        "building": "assembler",
        "ingredients": ["1 organic_crystal", "3 titanium_ingot"],
        "craft_speed": 4,
        "output": 1,
    },
    "titanium_glass": {
        "building": "assembler",
        "ingredients": ["2 glass", "2 titanium_ingot", "2 water"],
        "craft_speed": 5,
        "output": 2,
    },
    "turbine": {
        "building": "assembler",
        "ingredients": ["2 electric_motor", "2 magnetic_coil"],
        "craft_speed": 2,
        "output": 1,
    },
    "white_cube": {
        "building": "matrix lab",
        "ingredients": [
            f"1 {i}"
            for i in [
                "blue_cube",
                "red_cube",
                "yellow_cube",
                "purple_cube",
                "green_cube",
                "antimatter",
            ]
        ],
        "craft_speed": 15,
        "output": 1,
    },
    "yellow_cube": {
        "building": "matrix lab",
        "ingredients": ["1 diamond", "1 titanium_crystal"],
        "craft_speed": 8,
        "output": 1,
    },
}


def dsp_calc(
    desired_flow: float = 30.0,
    recipe_output: int = 1,
    resource_list: List[int] = [1],
    base_recipe_speed: float = 1.0,
    building_production_speed_factor: float = 1.0,
    proliferator_level: int = 3,
    building: str = "building",
    resources_name_list: Optional[List[str]] = None,
) -> np.ndarray:
    resource_list = np.array(resource_list)

    craft_speed = base_recipe_speed / building_production_speed_factor

    resources_consumption_per_building = (
        resource_list / craft_speed
    )  # products per second

    proliferated_output = recipe_output * proliferate_dict[proliferator_level]
    output_flow_per_building = proliferated_output / craft_speed  # products per second

    n_buildings = desired_flow / output_flow_per_building
    n_buildings = int(-(-n_buildings // 1))  # rounded up

    if building == "ray receiver":
        resources_consumption = n_buildings * resource_list
    else:
        resources_consumption = n_buildings * resources_consumption_per_building

    if resources_name_list is None:
        resources_name_list = [f"Resource {i+1}" for i in range(len(resource_list))]

    print(f"{n_buildings} {building} required")
    print("Will consume:")
    time_u = "per second"
    if building == "ray receiver":
        time_u = ""
    for i, n in enumerate(resources_consumption):
        print(f"\t{resources_name_list[i]}: {n:>10.3f} {time_u}")

    return n_buildings, resources_consumption


def full_dsp_calc(
    item: str,
    desired_flow: float = 30.0,
    assembler_level: int = 3,
    smelter_level: int = 2,
    proliferator_level: int = 3,
    total_dict: Dict = {"buildings": {}, "ingredients": {}},
):
    if item not in item_dict:
        raise Exception(f"No {item} in the item dictionary")

    n_ingredient_list = [int(i.split()[0]) for i in item_dict[item]["ingredients"]]
    ingredient_list = [i.split()[1] for i in item_dict[item]["ingredients"]]

    building = item_dict[item]["building"]
    if building == "assembler":
        building = f"assembler{assembler_level}"
    if building == "smelter":
        building = f"smelter{smelter_level}"
    building_production_speed_factor = building_speed_dict[building]

    print(f"\nTo produce {desired_flow:>10.3f}  {item:>25}  per second:")
    n_buildings, ingredient_consumption_list = dsp_calc(
        desired_flow=desired_flow,
        recipe_output=item_dict[item]["output"],
        resource_list=n_ingredient_list,
        resources_name_list=ingredient_list,
        base_recipe_speed=item_dict[item]["craft_speed"],
        building_production_speed_factor=building_production_speed_factor,
        proliferator_level=proliferator_level,
        building=building,
    )

    if building not in total_dict["buildings"]:
        total_dict["buildings"][building] = 0
    total_dict["buildings"][building] += n_buildings

    for i, ingredient in enumerate(ingredient_list):
        if ingredient not in total_dict["ingredients"]:
            total_dict["ingredients"][ingredient] = 0
        total_dict["ingredients"][ingredient] += ingredient_consumption_list[i]

        if ingredient in item_dict:
            total_dict = full_dsp_calc(
                ingredient,
                desired_flow=ingredient_consumption_list[i],
                assembler_level=assembler_level,
                smelter_level=smelter_level,
                proliferator_level=proliferator_level,
                total_dict=total_dict,
            )

    return total_dict


def main():
    parser = argparse.ArgumentParser(
        description="Break down the number of buildings and resource flow needed to produce a given item at a given flow rate"
    )
    parser.add_argument("-i", "--item", help="the name of the target item")
    parser.add_argument(
        "-f",
        "--flow",
        type=float,
        default=30.0,
        help="Number of item per second to produce",
    )
    parser.add_argument(
        "-a",
        "--assembler-level",
        type=int,
        default=3,
        choices=[1, 2, 3],
        help="Assembler level, one of [1,2,3], 3 is assembler mk3 etc.",
    )
    parser.add_argument(
        "-s",
        "--smelter-level",
        type=int,
        default=2,
        choices=[1, 2],
        help="Smelter level, one of [1,2], 2 is for Smelter mk2",
    )
    parser.add_argument(
        "-p",
        "--proliferator-level",
        type=int,
        default=3,
        choices=[0, 1, 2, 3],
        help="Proliferator level, one of [0,1,2,3], 3 is for the blue proliferator, 0 is no proliferation, assumes extra products is selected in buildings",
    )
    parser.add_argument(
        "--show-items", action="store_true", help="show a list of item names"
    )
    args = parser.parse_args()

    if args.show_items:
        print("Implemented items:")
        print("\n".join(sorted(list(item_dict.keys()))))
        return

    total_dict = full_dsp_calc(
        args.item,
        args.flow,
        args.assembler_level,
        args.smelter_level,
        args.proliferator_level,
    )

    if "swarm_sphere_MW" in total_dict["ingredients"]:
        total_dict["ingredients"]["swarm_sphere_GW"] = (
            total_dict["ingredients"]["swarm_sphere_MW"] / 1000.0
        )
        del total_dict["ingredients"]["swarm_sphere_MW"]

    for metric in ["buildings", "ingredients"]:
        print(f"\nTotals for {metric}:")
        for key in sorted(list(total_dict[metric].keys())):
            if (metric == "ingredients") and (key != "swarm_sphere_GW"):
                time_u = "per second"
            else:
                time_u = ""
            print(f"\t{total_dict[metric][key]:>10.3f}  {key:<25}  {time_u}")


if __name__ == "__main__":
    main()
