#include "converter1.h"

void converter1::set_attributes(){
  out.set_timestep(SIM_STEP, sc_core::SC_SEC);
}

void converter1::initialize(){

}

void converter1::processing()
{
	double tmp_power = in.read();
	double tmp_vout = VREF_CTI;

	// Assume a fixed effciency,the advanced converter model can be updated in here
	double efficiency = 1;
        out.write(tmp_power*efficiency/tmp_vout);
}
