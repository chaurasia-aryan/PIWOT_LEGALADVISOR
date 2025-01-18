import React from 'react'
import Image from 'next/image'

const Toolbar = () => {
  const homeImage = 'home-icon.png'
  const chatImage = 'chat-icon.png'
  const dashboardImage = 'dashboard-icon.png'

  return (
    <div>
      <ul>
        <li>
          <Image src={homeImage} alt='Home-Icon'/>
          <p>Home</p>
        </li>

        <li>
          <Image src={dashboardImage} alt='Dashboard-Icon'/>
          Dashboard
        </li>

        <li>
          <Image src={chatImage} alt='Chat-Icon'/>
          Chat
        </li>
      </ul>
    </div>
  )
}

export default Toolbar
