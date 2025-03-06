import json
import os
from pprint import pprint


data = {'a': {'b': {'c': 1, 'd': 2}}, 'e': 3}
pprint(data, width=1)

example = {'e': 3}
example2 = {'e2': example}
pprint(example2, width =1)

def save_list_to_json(new_list, filename, overwrite_flag=False):
    """
    Save a list to a JSON file. If overwrite_flag == True and a file already exists,
    new entries are appended to the JSON, otherwise it is created new.

    Parameters:
    new_list (list): The list to save.
    filename (str): The name of the file to save the list to.
    
    Moritz Schaller 05.02.2025
    """

    # # Load existing data
    # try:
    #     with open(filename, "rt") as json_file:
    #         old_data = json.load(json_file)
    # except IOError:
    #     # print("Could not read file, starting from scratch")
    #     old_data = []
    
    # # Append new list to the existing list if wished
    # if overwrite_flag:
    #     new_data = new_list
    # else: 
    #     new_data = old_data + new_list
        
    # # print("Overwriting %s" % filename)
    # with open(filename, "wt") as fp:
    #     json.dump(new_data, fp, indent=4)
    
    if os.path.exists(filename) and not overwrite_flag:
        # Load existing data
        with open(filename, 'r') as json_file:
            existing_list = json.load(json_file)
        
        if not isinstance(existing_list, list):
            raise ValueError("Existing JSON data is not a list")
        
        # Append new dict to the existing dict
        new_list = existing_list + new_list
        # existing_dict_list.append(dictionary)
        
        # Save the updated dict back to the existing file
        with open(filename, 'w') as json_file:
            json.dump(new_list, json_file, indent=4)
    else:
        # Create a new file
        with open(filename, 'w') as json_file:
            json.dump(new_list, json_file, indent=4)
    
def load_list_from_json(filename):
    """
    Load a list from a JSON file.

    Parameters:
    filename (str): The name of the file to load the dictionary from.

    Returns:
    loaded_list: The list loaded from the JSON file.
    
    Moritz Schaller 03.02.2025
    """
    with open(filename, 'r') as json_file:
        loaded_list = json.load(json_file)
    return loaded_list

# =============================================================================
# %% DATA BASE LAYOUT
# =============================================================================

"""
This is the intended hierarchic layout of the data base following the AGCO
Systems Engineering approach where possible [SLxx] ...System Level

The (*)/(**) shows a starting point for a detail that is not put in the main
tree to make it easier readible.

A ... behind an object behind a certain level shows that there could be
multiple instances of such an object at the same level in a sort of group format
of instances with variable size.
    Example: "phases" includes one or multiple instances of "phase"
        (phase descripes a specific set of material, no matter if liquid or solid)

In (text) some examples or comments are given.

Compared to this top down overview, the examples are pretty much bottom up written
due to variable logic.

"""

# crop ... [SL1] (Wheat)
    # plattform ... [SL3] (Ideal CL 10)
            # subsystem ... [SL5] (Residue Management)
                # specific_process_application ... [SL6] (Tailboard)
                    # software... (STAR-CCM+, PyBullet+S1ode, LIGGGHTS)
                        # dataset_version... (v1.0 Christian Korn TUD PhD thesis xx.x.2020)
                            # particle_simulation_dataset (*)

# DETAIL (*):
# particle_simulation_dataset
    # general_info
        # intended_purpose
        # confidence of various parts and aspects
        # refferences ... (further leading to material, documentation, reference (lab/field test results, thesises)
            # Comment (Like "in this section of the thesis or in this specific lab test we compared simulation against reality with results and thoughts xyz")
            # Link/data (either direct upload to files like PDF, pptx, excl... or at least "link")
    # domains ...
        # phenomena ... (**)
        # phases ... (***)
        # domain_motions ...
        # spatial_discretization
        # temporal_discretization
        # solver

# DETAIL (**):
# phenomenon
    # general_info
    # sub_phenomena ...
        # general_info
        # spatial_discretization (if different from parent domain)
        # temporal_discretization (if different from parent domain)
        # solver (if different from parent domain)

# DETAIL (***): (all these fields/dicts depend on the software and don't have to be filled)
# lagrangian_phases ... 
    # general_particle_data
    # bodies ... (One phase could consist of multiple bodies, e.g. a wheat grain could consist of different spheres or cylinders)
        # geometrical_definition
        # specific_physic_constants
    # body_configuration (specifies the rules of how the bodies are combined to one phase - coordinate systems, dimensions etc.)
    # injection_conditions...
     # angular_velocity
     # particle_orientation
     # velocity
# eulerian_phases ... 
    # phase_constants
# wall_phases
    # specific_physic_constants
# phase_interactions ...
    # phase partners
    # specific_physic_constants ...
    


#%% First Example: SwingFlow Tailboard in CFD-DEM with Star-CCM+ (Christian Korn, partly based on PhD)

general_info_instance7 = {
    "info_string": "SwingFlow Tailboard in CFD-DEM with Star-CCM+ (Christian Korn, partly based on PhD)",
    "intended_purpose": "Understanding and Feasiblitly study of creating STAR CFD-DEM simulations for the Residue Management",
    "refferences": "*LINK OR DIRECT FILE FOR PHD, POWERPOINTS* - each with comments"
    }


#### Capsular straw in Star

# star specific interaction coefficients 
specific_physic_constants_instance1 = { 
    "youngs_modulus": 1, #[MPa]
    "poisson_coefficient": 0.45
}


CDF_instance1 = { # Continuous relative distribution function of Probability of occurrence [%] as function of height [m] 
    0.00: 0.0,
    0.004: 4.9,
    0.00935: 12.7,
    0.002365: 42.9,
    0.003488: 76.4,
    0.006144: 97.5,
    0.009974: 100.0
}

capsular_instance1 = {
    "radius": 0.0018,
    "height": CDF_instance1 # Same as example 1
}

geometrical_definition_instance1 = {
    "type": capsular_instance1
}
    
general_particle_data_instance1 = {
    "rho_p": 150, # Density of the capsular material [kg/m^3]
}

body_instance1 = {
    "geometrical_definition": geometrical_definition_instance1,
    "specific_physic_constants": specific_physic_constants_instance1,
    }

bodies_instance1 = {
    "bodie_1 / Capsular" : body_instance1,
    }

## Injection conditions

angular_velocity_instance1 = {
    "Condition": "Angular velocity",
    "Method": "Normally distributed",
    "Values": {
        "Minimum": [-125.0, -125.0, -125.0],  # rad/s
        "Maximum": [125.0, 125.0, 125.0],  # rad/s
        "Mean": [0.0, 0.0, 0.0],  # rad/s
        "Standard deviation": [125.0, 125.0, 125.0]  # rad/s
    }
}

particle_orientation_instance1 = {
    "Condition": "Particle orientation",
    "Method": "Uniformly distributed",
    "Values": {
        "Minimum": [0.0, 0.0, 0.0],  # rad
        "Maximum": [6.28, 6.28, 6.28]  # rad
    }
}

velocity_instance1 = {
    "Condition": "Velocity",
    "Method": "Normally distributed",
    "Values": {
        "Minimum": [10.0, 0.0, 0.0],  # m/s
        "Maximum": [40.0, 0.0, 0.0],  # m/s
        "Mean": [30.0, 0.0, 0.0],  # m/s
        "Standard deviation": [10.0, 0.0, 0.0]  # m/s
    }   
}

lagrangian_injector_instance1 = {
    "angular_velocity": angular_velocity_instance1,
    "particle_orientation": particle_orientation_instance1,
    "velocity": velocity_instance1   
}

lagrangian_injectors_instance1 = {
    "lagrangian_injector_1 / Chopper Inlet": lagrangian_injector_instance1
}

lagrangian_phase_instance1 = {
    "general_particle_data": general_particle_data_instance1,
    "bodies" : bodies_instance1,
    "body_configuration" : None, # Trivial case, one instance of the phase consists of only one body
    "lagrangian_injectors": lagrangian_injectors_instance1
    
}




## Create lagrangian phase dict based on physics constants and injection conditions

lagrangian_phases_instance1 = {
    "lagrangian_phase_1 / Capsular chopped wheat straw": lagrangian_phase_instance1,
}


### Wall

specific_physic_constants_instance2 = { 
    "youngs_modulus": None, #[MPa] I dont have information available right now
    "poisson_coefficient": None # I dont have information available right now
}


# pyBullet specific data of the wall

wall_phase_instance1 = {
    "specific_physic_constants": specific_physic_constants_instance2,
}

wall_phases_instance1 = {
    "wall_phase_1 / Sheet metal steel": wall_phase_instance1,
}

### Eulerian/Continuous phase Air

eulerian_phase_instance1 = {
    "rho_f": 1.18415, # Fluid density [kg/m³] - here air at sea level and 25°C as Star
    "mu_f": 18.5508e-6, # Dynamic fluid viscosity [Pa*s] - here air at sea level and 25°C has 18.5508 μPa·s as Star
    "p_f": 101325 # Reference pressure of the air [Pa] (connected to mu_f)
}

eulerian_phases_instance1 = {
    "eulerian_phase_1 / Air": eulerian_phase_instance1
}

### Phase interactions

phase_interaction_instance1 = {
    "partners":"Capsular chopped wheat straw <-> Capsular chopped wheat straw",
    "Method": "Linear spring",
    "Coeff. of static friction μ0 [-]": 0.4,
    "Coeff. of rolling resistance μR [-]": 0.01,
    "Coeff. of normal restitution essn [-]": 0.1,
    "Coeff. of tangential restitution esst [-]": 0.1,
    "Normal spring stiffness Kn [Nm]": 1000,
    "Tangential spring stiffness Kt [Nm]": 1000
}

phase_interaction_instance2 = {
    "partners":"Capsular chopped wheat straw <-> Sheet metal steel",
    "Method": "Linear spring",
    "Coeff. of static friction μ0 [-]": 0.22,
    "Coeff. of rolling resistance μR [-]": 0.01,
    "Coeff. of normal restitution essn [-]": 0.1,
    "Coeff. of tangential restitution esst [-]": 0.1,
    "Normal spring stiffness Kn [Nm]": 40000,
    "Tangential spring stiffness Kt [Nm]": 40000
}

phase_interactions_instance1 = {
    "phase_interaction_1 / particle-particle": phase_interaction_instance1,
    "phase_interaction_2 / particle-wall": phase_interaction_instance2
}
    


#### Put together phases

phases_instance1 = {
    "lagrangian_phases": lagrangian_phases_instance1,
    "wall_phases": wall_phases_instance1,
    "eulerian_phases": eulerian_phases_instance1,
    "phase_interactions": phase_interactions_instance1}


pprint(phases_instance1)





#### Phenonema domain 1 - Tailboard and Environment (Chopper Outlet -> Ground)


### phenomenon Dynamic fluid flow coupled with granular medium

general_info_instance1 = {
    "general_solving_approach": "CFD-DEM",
    "Other Specifications": None,
}


## sub_phenomenon Turbulence

general_info_instance2 = {
    "general_solving_approach": "Realizable $k-\\epsilon$ turbulence",
    "Turbulence Governing eq.": "URANS",
    "Turbulence model": "Realizable k − ϵ*",
    "Under-Relaxation Factor": "0.8*",
    "Other coefficients": "default",
    "Wall treatment": "Two-layer All y+*"
}

sub_phenomenon_instance1 = {
    "general_info": general_info_instance2,
    }


## sub_phenomenon DEM

general_info_instance3 = {
    "General Solving Approach": "STAR-CCM+ Mesh based DEM",
    "Other Specifications" : "Inner iterations, solver settings...."
}


sub_phenomenon_instance2 = {
    "general_info": general_info_instance3,
    }

## sub_phenomenon Particle drag force

general_info_instance4 = {
    "general_solving_approach": "Drag coefficient formulation by Clift et al.",
    "Projection method for particle area": "STAR-CCM+ internal method utilizing octahedrons",
}

sub_phenomenon_instance3 = {
    "general_info": general_info_instance4,
}


## sub_phenomenon Particle drag torque

general_info_instance5 = {
    "general_solving_approach": "Rotational drag coefficient formulation by Sommerfeld"
}

sub_phenomenon_instance4 = {
    "general_info": general_info_instance5,
}


## sub_phenomenon Coupled flow

general_info_instance6 = {
    "general_solving_approach": "One-way coupling between eulerian and lagrangian phase"
}

sub_phenomenon_instance5 = {
    "general_info": general_info_instance6,
}


spatial_discretization_instance1 = {
    "Integration": "2nd-order upwind, implicit",
    "Gradients": "Hybrid Gauss-LSQ"
}

temporal_discretization_instance1 = {
    "Integration": "1st-order implicit",
    "Physical time step": "0.001",
    "Inner Iterations": "2"
}


### Put phenomenom together

phenomenon_instance1 = {
    "general_info": general_info_instance1,
    "sub_phenomenon_1 / Turbulence": sub_phenomenon_instance1,
    "sub_phenomenon_2 / DEM": sub_phenomenon_instance2,
    "sub_phenomenon_3 / Particle drag force": sub_phenomenon_instance3,
    "sub_phenomenon_4 / Particle drag torque": sub_phenomenon_instance4,
    "sub_phenomenon_5 / Coupled flow": sub_phenomenon_instance5,
    }

phenoma_instance1 = {
    "phenomenon_1 / Dynamic fluid flow coupled with granular medium": phenomenon_instance1
}



### domain_motions

# Stationary domain
stationary_motion_instance1 = {
    "Equation": "Stationary"
}

# Constant rotation of spinners
constant_rotation_motion_instance1 = {
    "Equation": "$\\omega_{Spn}= 2 \\pi n_{Spn}$**, turning_speed_tailbord_spinners	166.5 radian/s"
}

# Sinusoidal rotation of deflectors
sinusoidal_rotation_motion_instance1 = {
    "Equation": """**ParameterName	Value**
amplitude_flap_centre	0.40142573 radian
amplitude_flaps_left_right	0.3665914 radian
turning_speed_engine_flaps	9.21533845 radian/s
**FieldFunctionName	Value**
Oscillation_flap_centre	-1*[$(amplitude_flap_centre)sin($(turning_speed_engine_flaps)$(Time))]
Oscillation_flap_left_right	-1*[$(amplitude_flaps_left_right)sin($(turning_speed_engine_flaps)$(Time))]-0.03490659"""
}


domain_motions_instance1 = {
    "Stationary_domain": stationary_motion_instance1,
    "constantRotation_spinners": constant_rotation_motion_instance1,
    "sinusoidalRotation_deflectors": sinusoidal_rotation_motion_instance1
}

solver_instance1 = {
    "Solver type": "STAR-CCM+ AMG linear solver",
    "Solver device": "CPU (singlethreading and parallel computing supported)"}

#### Put together domain(s)

domain_instance1 = {
    "phenoma": phenoma_instance1,
    "phases": phases_instance1,
    "spatial_discretization": spatial_discretization_instance1,
    "temporal_discretization": temporal_discretization_instance1,
    "domain_motions": domain_motions_instance1,
    "solver": solver_instance1
    }


pprint(domain_instance1)
save_list_to_json(domain_instance1, "example_1_star_domain_1.json", overwrite_flag=True)


domains_instance1 = {
    "domain_1 / Tailboard and Environment (Chopper Outlet -> Ground)": domain_instance1
    }

#### Put together particle_simulation_dataset

particle_simulation_dataset_instance1 = {
    "general_info": general_info_instance7,
    "domains": domains_instance1
    }







#%% Second Example: Premium Tailboard PyBullet + S1ode (Diploma thesis Moritz Schaller)

#### Capsular straw in PyBullet

general_info_instance15 = {
    "info_string": "Mockup Premium Tailboard as possible candidate for CR-29P in opensource simulation Python scripts utilizing Bullet physics engine and custom equation system based on Diploma thesis Moritz Schaller 'Alternative particle simulation methods for combine harvesters with actively controlled residue spreading device'",
    "intended_purpose": "Feasiblitly study for utilization of open source software based on a game physics engine as alternative to STAR CFD-DEM simulations for the Residue Management",
    "refferences": "*LINK OR DIRECT FILE FOR PHD, POWERPOINTS* - each with comments"
    }

# pyBullet specific data of the capsular straw
specific_physic_constants_instance2 = { 
    "lateralFriction_p": 0.1,  # Lateral Friction coefficient of the particles (PyBullet)
    "spinningFriction_p": 0.001,  # Spinning Friction coefficient of the particles (PyBullet)
    "rollingFriction_p": 0.001,  # Rolling Friction coefficient of the particles (PyBullet)
    "restitution_p": 0.5,  # Restitution coefficient of the particles (PyBullet)
    "linearDamping_p": 0,  # Linear damping coefficient of the particles (PyBullet) - permanent without contact
    "angularDamping_p": 0,  # Angular damping coefficient of the particles (PyBullet) - permanent without contact
    "contactStiffness_p": -1,  # Contact stiffness coefficient of the particles (PyBullet)
    "contactDamping_p": -1,  # Contact damping coefficient of the particles (PyBullet)
}


body_instance2 = {
    "geometrical_definition": geometrical_definition_instance1, # Same as example 1
    "specific_physic_constants": specific_physic_constants_instance2,
    }

bodies_instance2 = {
    "bodie_1 / Capsular" : body_instance2,
    }

lagrangian_phase_instance2 = {
    "general_particle_data": general_particle_data_instance1, 
    "bodies" : bodies_instance2,
    "body_configuration" : None, # Trivial case, one instance of the phase consists of only one body
    "lagrangian_injectors": lagrangian_injectors_instance1 # Same as example 1
    
}





## Create lagrangian phase dict based on physics constants and injection conditions

lagrangian_phases_instance2 = {
    "lagrangian_phase_1 / Capsular chopped wheat straw": lagrangian_phase_instance2,
}



# pprint(lagrangian_phases_instance2,width=1)

### Wall

specific_physic_constants_instance3 = { 
    "lateralFriction_p": 0.5,  # Lateral Friction coefficient of the particles (PyBullet)
    "spinningFriction_p": 0.001,  # Spinning Friction coefficient of the particles (PyBullet)
    "rollingFriction_p": 0.001,  # Rolling Friction coefficient of the particles (PyBullet)
    "restitution_p": 0,  # Restitution coefficient of the particles (PyBullet)
    "linearDamping_p": 0,  # Linear damping coefficient of the particles (PyBullet) - permanent without contact
    "angularDamping_p": 0,  # Angular damping coefficient of the particles (PyBullet) - permanent without contact
    "contactStiffness_p": -1,  # Contact stiffness coefficient of the particles (PyBullet)
    "contactDamping_p": -1,  # Contact damping coefficient of the particles (PyBullet)
}


# pyBullet specific data of the wall

wall_phase_instance2 = {
    "specific_physic_constants": specific_physic_constants_instance3,
}

wall_phases_instance2 = {
    "wall_phase_1 / Sheet metal steel": wall_phase_instance2,
}

### Eulerian/Continuous phase Air


#### Put together phases

phases_instance2 = {
    "lagrangian_phases": lagrangian_phases_instance1,  # same as example 1
    "wall_phases": wall_phases_instance1,
    "eulerian_phases": eulerian_phases_instance1, # same as example 1
    "phase_interactions": None} # interactions in pyBullet are attributes of specific phase and indirectly dependent on each other (in Star they are a separate object)

pprint(phases_instance2)



#### Phenonema domain 1 - Tailboard cutoff (Chopper Outlet -> Tailboard close AABB)

## Phenomenon 1 Rigid body simulation

general_info_instance8 = {
    "general_solving_approach": "Bullet SDK utilized via pyBullet v. 3.25 Python API - rigid body pipeline with Bullet implementation of GJK-EPA for collision detection and penetration estimation",
    "Other Specifications": None,
}


### Put phenomenom 1 together

phenomenon_instance2 = {
    "general_info": general_info_instance8,
    }


## Phenomenon 2 Particle drag force

general_info_instance10 = {
    "general_solving_approach": "Drag coefficient formulation by Clift et al.",
    "Projection method for particle area": "Custom Python implementation of an average consideration based on the theorem of Cauchy (Cauchy’s surface formula)",
    "comment": "Drag force calculation based on constant air velocity field. Can be turned of. It would make sense to implement a static rotational air velocity field arround spinners to mimic air flow and ignore drag calculation otherwise."
}

phenomenon_instance3 = {
    "general_info": general_info_instance10,
    }



phenoma_instance2 = {
    "phenomen_1 / Rigid body simulation": phenomenon_instance2,
    "phenomen_2 / Particle drag force": phenomenon_instance3
}


temporal_discretization_instance2 = {
    "Integration": "1st-order semi-implicit",
    "Physical time step": "0.0001",
    "Inner Iterations": "50"
}

### domain_motions

# Constant rotation of spinners
constant_rotation_motion_instance2 = {
    "Equation": "$\\omega_{Spn}= 2 \\pi n_{Spn}$**, default RPM: 700RPM"
}

# Sinusoidal rotation of deflectors
sinusoidal_rotation_motion_instance2 = {
    "Equation": "$\\alpha_{Def} = a_{Def} \\cdot \\sin(f_{Def} \\cdot 2 \\pi \\cdot t) + o_{Def}$**"
}


domain_motions_instance2 = {
    "Stationary_domain": stationary_motion_instance1, # same as example 1
    "constantRotation_spinners": constant_rotation_motion_instance2,
    "sinusoidalRotation_deflectors": sinusoidal_rotation_motion_instance2
}

solver_instance2 = {
    "Solver type": "Bullet solver pipeline: Semi-implicit Euler based on Projected Gauß-Seidel for constraints plus GJK-EPA for narrowphase collision and penetration",
    "Solver device": "CPU (singlethreading), GPU (discontinued)"}

#### Put together domain 1

domain_instance2 = {
    "phenoma": phenoma_instance2,
    "phases": phases_instance2,
    "temporal_discretization": temporal_discretization_instance2,
    "domain_motions": domain_motions_instance2,
    "solver": solver_instance2
    }

pprint(domain_instance2)
save_list_to_json(domain_instance2, "example_2_pybullet_domain_1.json", overwrite_flag=True)


#### Phenonema domain 2 - Environment (Particle flight trajectories from Tailboard close AABB -> Ground)

## Phenomenon 1 Point mass kinematic under influence of gravity and drag force based on distance based drag discount

general_info_instance11 = {
    "general_solving_approach": "S1ode - Python implementation of Newton's second law in 3D in form of a coupled system of six first-order ordinary differential equations",
    "Other Specifications": None,
}

## sub_phenomenon Point mass kinematic under gravity

general_info_instance12 = {
    "general_solving_approach": "S1ode - Python implementation of Newton's second law",
}

sub_phenomenon_instance6 = {
    "general_info": general_info_instance12,
    }

## sub_phenomenon Particle drag force

sub_phenomenon_instance7 = {
    "general_info": general_info_instance10, # Same as domain 1 Phenomenon 2 Particle drag force
    }

## sub_phenomenon Distance based drag discount

general_info_instance13 = {
    "General Solving Approach": "Introduction of a drag discount factor that increases with decreasing distance from the tailboard within an interval of 0 and 1",
    "Other Specifications": "Default start discount: 35% (that means particles see only 65% of the 'normal' drag force magnitude, and after a default distance of 5 m or more they see the normal 100% according to Clift et al.",
    "Comment": "Following concept suggestion of Diploma thesis, a spatially discretized drag discount model should be considered"
}


sub_phenomenon_instance8 = {
    "general_info": general_info_instance13,
    }

## sub_phenomenon Wind

general_info_instance14 = {
    "General Solving Approach": "Constant velocity field taken into account for particle slip velocity for calculation of particle drag forces",
    "Other Specifications" : None
}


sub_phenomenon_instance9 = {
    "general_info": general_info_instance14,
    }


### Put phenomenom together

phenomenon_instance4 = {
    "general_info": general_info_instance11,
    "sub_phenomenon_1 / Point mass kinematic under gravity": sub_phenomenon_instance6,
    "sub_phenomenon_2 / Particle drag force": sub_phenomenon_instance7,
    "sub_phenomenon_3 / Distance based drag discount": sub_phenomenon_instance8,
    "sub_phenomenon_4 / Wind": sub_phenomenon_instance9
    }

phenoma_instance2 = {
    "phenomenon_1 / Point mass kinematic under influence of gravity and drag force based on distance based drag discount": phenomenon_instance4
}


temporal_discretization_instance3 = {
    "Integration": "Explicit Runge-Kutta method of order 5(4) family as published in Dormand, J. R. ; Prince, P. J.: A family of embedded Runge-Kutta formulae. In: Journal of Computational and Applied Mathematics 6 (1980), Nr. 1, 19–26. http://dx.doi.org/10.1016/0771-050X(80)90013-3. – DOI 10.1016/0771–050X(80)90013–3. –ISSN 0377–0427",
    "Physical time step": "0.001",
}

solver_instance3 = {
    "Solver type": "Python SciPy module implementing a FORTRAN based code of Explicit Runge-Kutta method of order 5(4) family as published in Dormand, J. R. ; Prince, P. J.: A family of embedded Runge-Kutta formulae. In: Journal of Computational and Applied Mathematics 6 (1980), Nr. 1, 19–26. http://dx.doi.org/10.1016/0771-050X(80)90013-3. – DOI 10.1016/0771–050X(80)90013–3. –ISSN 0377–0427",
    "Solver device": "CPU (singlethreading)"}

#### Put together domain 2

domain_instance3 = {
    "phenoma": phenoma_instance2,
    "phases": phases_instance2,
    "temporal_discretization": temporal_discretization_instance3,
    "domain_motions": None,
    "solver": solver_instance3
    }

pprint(domain_instance3)
save_list_to_json(domain_instance3, "example_2_s1ode_domain_2.json", overwrite_flag=True)

domains_instance2 = {
    "domain_1 / Tailboard cutoff (Chopper Outlet -> Tailboard close AABB)": domain_instance2,
    "domain_2 / Environment (Particle flight trajectories from Tailboard close AABB -> Ground)": domain_instance3
    }

#### Put together particle_simulation_dataset

particle_simulation_dataset_instance2 = {
    "general_info": general_info_instance15,
    "domains": domains_instance2
    }


#%% Uniting both examples into entire/rest data structure

#### Put together rest of the data base hierachy up to Crops


#### data sets
data_set_version_instance1 = {
    "version": "v1.0 Christian Korn TUD PhD thesis xx.x.2020",
    "particle_simulation_dataset": particle_simulation_dataset_instance1}

data_set_version_instance2 = {
    "version": "v1.0 Moritz Schaller Diploma thesis 30.09.2024",
    "particle_simulation_dataset": particle_simulation_dataset_instance2}


#### softwares

software_instance1 = {
    "software_name": "Simcenter StarCCM+ by Siemens PLM Software",
    "software_version": "v.18.06.007 resp. 2310.0001",
    "data_set_version": data_set_version_instance1
    }

software_instance2 = {
    "software_name": "PyBullet-S1ode pipeline by Moritz Schaller",
    "software_version": "v.1.0",
    "data_set_version": data_set_version_instance2
    }

#### specific process applications

specific_process_application_instance1 = {
    "software_1 / STAR": software_instance1,
    "software_2 / PyBullet-S1ode": software_instance2
    }

#### subsystems

subsystem_instance1 = {
    "specific_process_application_1 / Tailboard": specific_process_application_instance1,
    }


#### plattforms

plattform_instance1 = {
    "subsystem_1 / Residue Management": subsystem_instance1
    }

#### crops

# Crop instance 1 would then be weed
crop_instance1 = {
    "plattform_1 / Ideal CL10": plattform_instance1}

# Crop instance 1 would then be weed
crops_instance1 = {
    "crop 1 / wheat": crop_instance1}

pprint(crop_instance1)
save_list_to_json(crops_instance1, "crops_instance1.json", overwrite_flag=True)