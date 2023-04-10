const puppeteer = require('puppeteer')
const readline = require("readline")
const fs = require('fs').promises
const util = require('util')

async function detecteXSSReflechie(url, payload, headlessBool) {
  const browser = await puppeteer.launch({
    headless: headlessBool, // option pour afficher le navigateur
  })

  const page = await browser.newPage()
  await page.goto(url)

  // Pour trouver un input qui soit un texte, il faut prendre en considération qu'il n'a peut-être pas
  // le "type = text" donc on le définit par exclusion des autres types ou par textarea.
  // Généralement les balises vulnérables à une xss sont input et textarea donc on ajoute aussi textarea
  const inputElements = await page.$$( 
    'input:not([type="submit"]):not([type="button"]):not([type="reset"]):not([type="hidden"]), textarea'
  )

  let xssDetected = false

  for (const inputElement of inputElements) {
    await inputElement.type(payload) // pour chaque élément trouvé on y tape la payload 
  }

  await page.click('input[type="submit"]')

  const dialogPromise = new Promise((resolve) => { 
    page.on('dialog', async dialog => { // Si une alert apparaît la XSS est valide
      console.log('La page est vulnérable à une XSS détectée : '+payload)
      xssDetected = true
      resolve()
    })
  })

  await Promise.race([ // On attend soit que la promesse de détection de XSS soit résolue, soit qu'une courte période se soit écoulée (pour chaque xss)
    dialogPromise,
    new Promise(resolve => setTimeout(resolve, 200))
  ])

  if(!xssDetected || headlessBool) // Si on est en mode terminal et qu'on trouve une xss, on va laisser le browser ouvert pour voir l'injection qui a marché
    await browser.close()

  return xssDetected
}


async function run() {
  let affichage = true // variable headless pour afficher ou pas le navigateur

  console.log("########### Détecteur de XSS Réfléchie ###########")

  const inquirer = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  })

  const questionH = util.promisify(inquirer.question).bind(inquirer)

  async function questionHeadless() {
    const bool = await questionH("Voulez-vous afficher les exécutions faites sur le navigateur ? (O/N) ")
    if (bool.toUpperCase() === "O") {
      affichage = false
      console.log("Ouverture du navigateur !")
    }
    else {
      console.log("Mode terminal")
    }
    inquirer.close()
  }

  await questionHeadless()
  // La liste des payloads est une partie des payloads de https://github.com/payloadbox/xss-payload-list/blob/master/Intruder/xss-payload-list.txt
  const data = await fs.readFile('xss-payload-list.txt', 'utf8')
  const payloads = data.split('\n')
  console.log("Fire !")

  let b = false

  for (const payload of payloads) {
    // Ce site fourni par Google est expréssemment vulnérable à la xss basique (utile pour le test)
    b = await detecteXSSReflechie('https://xss-game.appspot.com/level1/frame', payload, affichage)
    if(b==true)
      break
  }

  if(b==false)
    console.log("Aucune xss trouvée sur le site")

} 

run()