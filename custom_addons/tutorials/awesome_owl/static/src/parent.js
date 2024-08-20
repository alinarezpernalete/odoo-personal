/** @odoo-module **/

import { Component, xml, useState } from "@odoo/owl";
import { Playground } from "./playground";
import { Card } from "./card";

export class Parent extends Component {
    static template = xml`
        <div>
            <Playground/>
            <Card title="state.a" content="state.b"/>
            <Card title="state.c" content="state.d"/>
        </div>
    `;

    static components = { Playground, Card };
         
    state = useState({ 
        a: "card 1",
        b: "content of card 1",
        c: "card 2",
        d: "content of card 2"
    });
    
}