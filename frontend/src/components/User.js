import React from "react"
import { IoCloseCircleSharp, IoHammerSharp } from "react-icons/io5"
//import AddUser from "./AddUser"

class User extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            editForm: false
        }}
    user = this.props.user
    render() {
           return (
                <div className="block_user">
                    <IoCloseCircleSharp onClick={() => this.props.onDelete(this.user.id)} className="delete-icon" />
                    <IoHammerSharp onClick={
                                    () => {this.setState({editForm: !this.state.editForm})}
                                   } 
                                   className="edit-icon" />
                    <h3>{this.user.last_name} {this.user.first_name}</h3>
                    <p>{this.user.age}</p>
                    <img src={this.user.avatar} alt='description1' />
                    <b>{this.user.isHappy ? 'Счастлив :)' : 'Не особо :('}</b>
                    {this.state.editForm && <AddUser user={this.user} onAdd={this.props.onEdit} />}
                </div>
           )
    }
}

export default User