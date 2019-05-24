import React,{Component} from 'react'
import ReactDOM from 'react-dom'
import request from 'superagent'
import './style.css'

import CARDS from './component/cards.js'

class Main extends Component{

    constructor(props){
        super(props);
        this.state = {
            "player0": [],
            "player1": [],
            "player2": [],
            "player3": [],
            "field":[],
            "turn": 0,
            "reverse": false,
            "back": false,
            "rank": [-1,-1,-1,-1]
        };
    }

    game(e){

        request.post('/game')
        .send({"start":false})
        .end(
            (error, res) => {
                if (!error && res.status === 200) {
                    
                    var json_data = JSON.parse(res.text);
                    this.setState(json_data);
    
                } else {
                    console.log(error);
                }
            }
        );

    }
    
    componentDidMount(){
        
        console.log("check");

        request.post('/game')
        .send({"start":true})
        .end(
            (error, res) => {
                if (!error && res.status === 200) {
                    
                    var json_data = JSON.parse(res.text);
                    this.setState(json_data);
    
                } else {
                    console.log(error);
                }
            }
        );
    }

    render(){
        
        var border_name = ["bottom","left","top","right"];
        var border_pos = "border_"+border_name[this.state.turn];
        console.log(border_pos);

        return(
            <div id="container">
                <div id="table" onClick={(e)=>this.game(e)} className={border_pos}>
                    
                    {this.state["field"]==[]?<div/>:
                    <img 
                        src={CARDS[this.state["field"].slice(-1)]}
                        alt="" 
                        width={"100px"} 
                        height={"140px"}
                        style = {{"position":"absolute","left":"350px","top":"350px"}}
                    />}

                    <Player card={this.state["player0"]} number={0} left={"50px"} top={"600px"} bg_color={this.state.turn==0?"#FF0000":"#AA33FF"}/>
                    <Player card={this.state["player1"]} number={1} left={"-200px"} top={"450px"} bg_color={this.state.turn==1?"#FF0000":"#AA33FF"}/>
                    <Player card={this.state["player2"]} number={2} left={"-50px"} top={"200px"} bg_color={this.state.turn==2?"#FF0000":"#AA33FF"}/>
                    <Player card={this.state["player3"]} number={3} left={"200px"} top={"350px"} bg_color={this.state.turn==3?"#FF0000":"#AA33FF"}/>
                </div>
            </div>
        );  
    }
}


const Player = (props)=>{

    
    var deg = (90*props.number).toString();
    var arr = Array.apply(null, {length: props.card.length}).map(Number.call, Number);
    
    return(
        <div className="player" style={{"transform":"rotate("+deg+"deg)", "left":props.left, "top":props.top}}>
            {arr.map( (i)=>
                <img 
                    src={CARDS[props.card[i]]} 
                    alt="" 
                    width={"100px"} 
                    height={"140px"} 
                    key={i} 
                    style={{"left":(30*i).toString()+"px"}} 
                /> 
            )}
        </div>
    );
}


ReactDOM.render(
    <Main />,
    document.getElementById('root')
);