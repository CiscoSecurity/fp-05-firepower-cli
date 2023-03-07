import { useState } from 'react';

export default function Table(props) {

  return (
            <div class="col-md-12">
              <div class="panel">
                <div class="table-admins">
                  <h3>Output Types</h3>
                  <table class="table">
                    <thead>
                      <tr class="table__header-row">
                        <th class="table__header-cell">Output Type</th>
                        <th class="table__header-cell">Destination</th>
                        <th class="table__header-cell table__header-cell--align-center">Active</th>
                        <th class="table__header-cell table__header-cell--align-right">Last Data Sent</th>
                        <th class="table__header-cell table__header-cell--align-right">Action</th>
                      </tr>
                    </thead>
		      <tbody>
    			<tr class="table__row">
			   <td class="table__cell">post</td>
    			</tr>
                     </tbody>
                   </table>
                </div>
              </div>
            </div>
  );
}
