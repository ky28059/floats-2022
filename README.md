# floats-2022
All the code for the 2022 Junior float. 

This year's electrical components include the opening and closing hatch, the fog machine, the radio, the monitor, and the 
LED lights. Mechanically, these systems are connected like so:
```mermaid
graph TD;
    Pi(Raspberry Pi)-->|HDMI|Monitor;
    Pi-->|Aux|Radio;
    Pi-->|GPIO port 33|TalonSRX;
    TalonSRX-->CIM;
    T{{120V->12V Transformer}}-.->TalonSRX;
    E1{{Extension Cord 1}}-.->T;
    Pi-->|GPIO port 29|L1[Limit Switch 1];
    Pi-->|GPIO port 31|L2[Limit Switch 2];
    Pi-->LEDs;
    Pi-->Relay;
    Relay-->F[Fog Machine];
    E2{{Extension cord 2}}-.->Relay;
    E1-.->Pi;
    E1-.->Monitor;
    E1-.->Radio;
```
