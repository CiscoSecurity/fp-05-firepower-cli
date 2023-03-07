import React from 'react';

class SideBar extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div class="sidebar-container">
          <div class="sidebar sidebar--bg-gray">
            <div class="sidebar__header">
              <div class="sidebar__title">Monitoring</div>
              <a class="sidebar__list-menu">
                <span class="icon icon-list-menu"></span>
              </a>
            </div>
            <ul>
              <li tabindex="0" class="sidebar__item"><a class="sidebar__link">Live Dashboard</a></li>
              <li class="sidebar__drawer sidebar__drawer--opened">
                <a tabindex="0" class="sidebar__link"><span class="icon icon-chevron-down"></span>Secure Firewall</a>
                <ul>
                  <li tabindex="0" class="sidebar__item"><a class="sidebar__link">Application Status</a></li>
                  <li tabindex="0" class="sidebar__item sidebar__item--selected"><a class="sidebar__link">Configuration</a></li>
                  <li class="sidebar__drawer sidebar__drawer--opened">
                    <a tabindex="0" class="sidebar__link"><span class="icon icon-chevron-down"></span>SIEM integrations</a>
                    <ul>
                      <li tabindex="0" class="sidebar__item"><a class="sidebar__link">OCSF (json)</a></li>
                      <li tabindex="0" class="sidebar__item"><a class="sidebar__link">AWS Data Lake</a></li>
                      <li tabindex="0" class="sidebar__item"><a class="sidebar__link">Splunk</a></li>
                      <li tabindex="0" class="sidebar__item"><a class="sidebar__link">Sentinel</a></li>
                    </ul>
                  </li>
                </ul>
              </li>
              <li class="sidebar__drawer">
                <a tabindex="0" class="sidebar__link"><span class="icon icon-chevron-right"></span>FAQ</a>
                <ul>
                  <li tabindex="0" class="sidebar__item"><a class="sidebar__link">Usage</a></li>
                  <li tabindex="0" class="sidebar__item"><a class="sidebar__link">Documentation</a></li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
    );
  }
}

export default SideBar;
