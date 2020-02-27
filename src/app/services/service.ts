import { Injectable } from '@angular/core';
import { Observable, forkJoin, BehaviorSubject } from 'rxjs';
import { ModePaiement } from '../interface/modePaiement-interface';
import { HttpClient } from '@angular/common/http';
import { Etat } from '../interface/etat-interface';
import { FraisForfait } from '../interface/fraisForfait-interface';
import { LigneFraisForfait } from '../interface/ligneFraisForfait-interace';
import { share } from 'rxjs/operators';
import { AuthenticationService } from '../services/authentication.service'

@Injectable({
  providedIn: 'root'
})
export class ServiceService {

  constructor(private http: HttpClient,public auth: AuthenticationService) { }

  modePaiement = []
  fraisForfait = []
  ligneFraisForfait = []
  etat = []
  config = new BehaviorSubject<any>({});
  adress = "" //LOCAL
  // adress = "http://wlfusion03s.priv.birdz.com:5000/" //DEV 
  init() {
    forkJoin(
      this.getModePaiement(),
      this.getFraisForfait(),
      // this.getLigneFraisForfait(this.auth.getUserDetails.v);
    ).subscribe(() => {
      this.config.next({
        modePaiement: this.modePaiement,
        fraisForfait: this.fraisForfait,
      })
    })

  }

  getModePaiement(): Observable<ModePaiement[]> {
    const req = this.http.get<ModePaiement[]>(this.adress + 'users/mode_paiement').pipe(share());
    req.subscribe((res => {
      res.forEach((item) => {
        this.modePaiement[item.id] = {
          id: item.id,
          modePaiement: item.modePaiement,
        }
      })
    }));
    return req;
  }

  getEtat(): Observable<Etat[]> {
    return this.http.get<Etat[]>(this.adress + 'users/etat');
  }

  getFraisForfait(): Observable<FraisForfait[]> {
    const req = this.http.get<FraisForfait[]>(this.adress + 'users/frais_forfait').pipe(share());
    req.subscribe((res => {
      res.forEach((item) => {
        this.fraisForfait[item.id] = {
          id: item.id,
          libelle: item.libelle,
          montant: item.montant,
        }
      })
      console.log("res", res)
    }));
    return req;
  }

  getLigneFraisForfait(idVisiteur): Observable<LigneFraisForfait[]> {
    const req = this.http.get<LigneFraisForfait[]>(this.adress + 'users/ligne_frais_forfait?num=' + idVisiteur).pipe(share());
    req.subscribe((res => {
      res.forEach((item) => {
        this.fraisForfait[item.idVisiteur] = {
         idVisiteur : item.idVisiteur,
         mois : item.mois,
         idFraisForfait : item.idFraisForfait,
         quantite : item.quantite,
        }
      })
      console.log("res", res)
    }));
    return req;
  }


  sendMail(fraisForfait: FraisForfait[], ligneFraisForfait: LigneFraisForfait): Observable<FraisForfait[]> {
    const body = {
         fraisForfait, 
         ligneFraisForfait
    }
    return this.http.put<FraisForfait[]>(this.adress + 'api/mail', body);
}
}


