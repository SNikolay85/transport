import React from "react"
import Header from "./Header"
import Image from "./Image"
import logo from "../img/logo512.png"

class App extends React.Component {
       constructor(props) {
              super(props)
              this.state = {
                     helpText: 'Help text',
                     userData: ''
              }
       this.inputClick = this.inputClick.bind(this)
       }

       render() {
              return(
                     <div className='name'>
                            <Header my_text='Шапка сайта' />    
                            <Header my_text='Еще шапка!!!' />    
                            <h1>{this.state.helpText}</h1>
                            <h2>{this.state.userData}</h2>
                            <input placeholder={this.state.helpText}   
                                   onChange={event => this.setState({userData: event.target.value})}     
                                   onClick={this.inputClick} 
                                   onMouseEnter={this.mouseOver} />
                     <p>{this.state.helpText === 'Help text!' ? 'Yes' : 'No'}</p>  
                     <Image my_image={logo} alt='description1' />
                     <img className='logo_pic' src={logo} alt='description2' />  
                     </div>)   
       }   
       inputClick() {
              this.setState({helpText: 'changed'})
              console.log('Clicked')
       }
       mouseOver() {console.log('Mouse Over')}
}

export default App
