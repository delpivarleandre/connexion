import { Component, OnInit } from '@angular/core';
import { ServiceService } from '../services/service'
import { ModePaiement } from '../interface/modePaiement-interface';
import { FraisForfait } from '../interface/fraisForfait-interface';
import { AuthenticationService } from '../services/authentication.service';

@Component({
  selector: 'app-ajout-frais',
  templateUrl: './ajout-frais.component.html',
  styleUrls: ['./ajout-frais.component.scss']
})
export class AjoutFraisComponent implements OnInit {

  constructor( private service: ServiceService,
    public auth: AuthenticationService) { }
  modePaiementOptions : ModePaiement[]
  fraisForfaitOptions : FraisForfait[]
  ngOnInit() {
      this.modePaiementOptions = this.service.modePaiement.filter(r => r);
      this.fraisForfaitOptions = this.service.fraisForfait;
    console.log(this.service.fraisForfait)
    console.log(this.fraisForfaitOptions)
    console.log(this.modePaiementOptions)
    console.log(this.auth.getUserDetails())
    console.log(this.auth.getUserDetails().)
  }
}
