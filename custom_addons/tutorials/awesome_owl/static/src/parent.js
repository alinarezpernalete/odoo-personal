/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { Playground } from "./playground";

export class Parent extends Component {
    static template = xml`
        <div>
            <Playground/>
            <Playground/>
            <Playground/>
            <Playground/>
            <Playground/>
        </div>
    `;

    static components = { Playground };
}