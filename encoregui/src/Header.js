import React from 'react';

class Header extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <header class="header">
        <a tabindex="0" class="header__logo">
        <span class="icon-cisco"></span>
        </a>
        <div tabindex="0" class="header__title">
          <h2>eNcore eStreamer Management Portal</h2>
        </div>
        <div class="header__navigation">
          <ul class="tab-group">
            <li tabindex="0" class="tab-group__tab">
              <a class="tab-group__link">Home</a>
            </li>
          </ul>
        </div>
        <div class="header__toolbar">
          <a tabindex="0" class="header__icon">
            <span class="icon icon-search"></span>
          </a>
          <a tabindex="0" class="header__icon">
            <span class="icon icon-alert"></span>
          </a>
          <a tabindex="0" class="header__icon">
            <span class="icon icon-help"></span>
          </a>
          <a tabindex="0" class="header__icon" onclick="openPopover()">
            <span class="icon icon-user"></span>
          </a>
        </div>
      </header>
    );
  }
}

export default Header;
