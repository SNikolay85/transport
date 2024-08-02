import React from "react"
// import Button from "./Button"

class Header extends React.Component {
    render() {
           return (
           <header className='header'>
                {this.props.my_text}
            </header>
           )
    }
}

export default Header