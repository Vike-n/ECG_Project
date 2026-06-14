# ECG Project | Under Development

This repository contains the hardware design, schematics, and simulation files for an electrocardiogram (ECG) signal acquisition and conditioning system developed for academic purposes.

The system is focused on capturing bio-physiological signals, featuring instrumentation amplification, filtering, and digital processing of the signals. This proyect also covers the power supply and basics protections of the system.

## Key Features

* **Biomedical Instrumentation:** Design optimized for microvolt-level differential heart signals.
* **Analog Filtering Stage:**
  * **High-Pass Filter (HPF):** Removes DC offsets and baseline wandering.
  * **Twin-T Notch Filter:** Attenuates 50Hz powerline interference.
  * **Low-Pass Filter (LPF):** Bessel response stage to minimize phase distortion and high-frequency noise.
* **Supply** Designed for rechargable batteries featuring portability.  
* **ECG Simulations:** Complete validation using LTspice `.asc` models for AC analysis and transient response.
* **Hardware Layout:** PCB design and schematics built entirely using KiCad.

## Future Features
* **ESP 32**
  * Analog to digital conversion of the sensed signal.
  * Digital processing.
  * Wierless transmission to a phone or PC.

## Repository Structure

* `📂 /KiCAD/` Main KiCad project files (`.kicad_pro`, `.kicad_sch`, `.kicad_pcb`).
* `📂 Simulation/`: LTspice schematic files (`.asc`) and verification testbenches.
* `📂 Docs/`: Technical reports, documentation, and asset files.

## Software Requirements

To open and interact with the source files in this repository, you will need:
* **KiCad (v6.0 or newer):** For schematics and PCB layout visualization.
* **LTspice:** For running the analog circuit simulation topologies.

## Clone & Usage

To replicate or review the project locally, clone this repository:
```bash
git clone [https://github.com/Vike-n/ECG_Project.git](https://github.com/Vike-n/ECG_Project.git)
