import React from "react"
import Header from "./Header"
import Users from "./Users"
import AddUser from "./AddUser"
import axios from "axios"

const baseurl = "http://127.0.0.1:8000/people/"
//const baseurl = "https://reqres.in/api/users?page=2"
class Les7 extends React.Component {
       constructor(props) {
              super(props)

               axios.get(baseurl).then((res) => {
                      this.setState({users: res.data.peoples })
               })
//              axios.get(baseurl).then((res) => {
//                     console.log(res.data.peoples)
//              })

              this.state = {
                   users: [
              //         {
              //             "id": 1,
              //             "first_name": "Bob", 
              //             "last_name": "Marley", 
              //             "patronymic": "mc",
              //             "age": 25,
              //             "isHappy": true
              //         },
              //         {
              //             "id": 2,
              //             "first_name": "Jack", 
              //             "last_name": "Richer", 
              //             "patronymic": "vc",
              //             "age": 40,
              //             "isHappy": false
              //         }
                  ]
              }
              this.addUser = this.addUser.bind(this)
              this.deleteUser = this.deleteUser.bind(this)
              this.editUser = this.editUser.bind(this)
      
          }
       render() {
              return(
                     <div>
                            <Header my_text='Список пользователей' />    
                            <div className="main_form">
                                <Users users={this.state.users} onEdit={this.editUser} onDelete={this.deleteUser} />
                            </div> 
                            <aside>
                                   <AddUser onAdd={this.addUser} />
                            </aside>
                     </div>)   
       }  

       addUser(user) {
              const id = this.state.users.length + 1
              this.setState({
                     users: [...this.state.users, {id, ...user}]
              })
       }

       editUser(user) {
              let allUsers = this.state.users
              allUsers[user.id - 1] = user

              this.setState({users: []}, () => {
                     this.setState({users: [...allUsers]})
              })
       }

       deleteUser(id) {
              this.setState({
                     users: this.state.users.filter((user) => user.id !== id)
              })
       }
}

export default Les7
