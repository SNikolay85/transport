import React from 'react'
import Header from './Header'
import Drivers from './Drivers'
import ListDrivers from './ListDrivers'
import axios from 'axios'

const baseurl = 'http://127.0.0.1:8000'

class AppRoute extends React.Component

    {
        constructor(props)
            {
              super(props)

               axios.get(baseurl+'/driver/').then((res) => {
                      this.setState({drivers: res.data.drivers })
               })

               this.state = {drivers: []}
            }
       render() {
          return(
             <div>
                <Header my_text='Добавление поездок' />
                <div className="main_form">
                    <Drivers drivers={this.state.drivers} />
                </div>
                <aside>
                   <ListDrivers drivers={this.state.drivers} />
                </aside>
             </div>)
       }
    }

export default AppRoute