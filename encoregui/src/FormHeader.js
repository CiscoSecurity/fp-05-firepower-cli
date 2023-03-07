import React from 'react';

class FormHeader extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
          <div class="steps">
	    <div id="step0" class="step">
	      <div class="step__icon">1</div>
	      <div class="step__content">
	        <div class="step__label"><span class="step__title">Authorize Endpoint</span></div>
	        <div class="step__hint">Create a certificate on the FMC using "this" host ip or fqdn</div>
	      </div>
	    </div>
	    <div id="step1" class="step">
	      <div class="step__icon">2</div>
	      <div class="step__content">
	        <div class="step__label"><span class="step__title">Configuration Details</span></div>
	        <div class="step__hint">Specify FMC configuration Info Below</div>
	      </div>
	    </div>
	    <div id="step2" class="step active">
	      <div class="step__icon">3</div>
	      <div class="step__content">
	        <div class="step__label"><span class="step__title">Test Connectivity</span></div>
	        <div class="step__hint">In the table below click "Start" Command to test connectivity and start generating data</div>
	      </div>
	    </div>
	    <div id="step3" class="step">
	      <div class="step__icon">4</div>
	      <div class="step__content">
	        <div class="step__label"><span class="step__title">Monitor</span></div>
	        <div class="step__hint">Monitor the eNcore logs to ensure continous event streaming</div>
	      </div>
           </div>
	 </div>
    );
  }
}

export default FormHeader;

