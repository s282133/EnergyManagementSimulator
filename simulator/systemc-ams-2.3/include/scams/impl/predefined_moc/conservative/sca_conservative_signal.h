/*****************************************************************************

    Copyright 2010
    Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V.

    Copyright 2015-2016
    COSEDA Technologies GmbH

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

 *****************************************************************************/

/*****************************************************************************

  sca_conservative_signal.h - description

  Original Author: Karsten Einwich Fraunhofer IIS/EAS Dresden / COSEDA Technologies

  Created on: 04.11.2009

   SVN Version       :  $Revision: 1892 $
   SVN last checkin  :  $Date: 2016-01-10 11:59:12 +0000 (Sun, 10 Jan 2016) $
   SVN checkin by    :  $Author: karsten $
   SVN Id            :  $Id: sca_conservative_signal.h 1892 2016-01-10 11:59:12Z karsten $

 *****************************************************************************/

/*****************************************************************************/


#ifndef SCA_CONSERVATIVE_SIGNAL_H_
#define SCA_CONSERVATIVE_SIGNAL_H_

namespace sca_core
{
namespace sca_implementation
{


class sca_conservative_signal :
	public sca_core::sca_prim_channel,
	virtual public sca_core::sca_implementation::sca_conservative_interface
{
 public:

    sca_conservative_signal();
    explicit sca_conservative_signal(const char* _name);

    virtual const char* kind() const;

    bool ignore_node() const;

    virtual long get_node_number() const;
    virtual double* get_result_ref();

    /**
      * returns one connected module if available,
      * otherwise NULL is returned
      */
     sca_conservative_module* get_connected_module();

 protected:


    friend class sca_conservative_view;

    long node_number;
    long equation_id;
    bool reference_node;
    long cluster_id;
    bool connects_cviews;

 private:

    void construct();

	/** method of interactive tracing interface, which returns the value
		 * at the current SystemC time (the time returned by sc_core::sc_time_stamp())
		 */
    virtual const double& get_typed_trace_value() const;

};

}
}


#endif /* SCA_CONSERVATIVE_SIGNAL_H_ */
