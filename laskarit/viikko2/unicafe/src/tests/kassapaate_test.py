import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
  def setUp(self):
    self.kassapaate = Kassapaate()
    self.kortti = Maksukortti(1000)

  def test_luodun_kassapaatteen_kassassa_on_oikea_summa_rahaa(self):
    self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

  def test_luodun_kassapaatteen_myytyjen_lounaiden_maara_on_oikein(self):
    self.assertEqual(self.kassapaate.edulliset, 0)
    self.assertEqual(self.kassapaate.maukkaat, 0)

  def test_syo_edullisesti_kateisella_palauttaa_vaihtorahat_oikein(self):
    self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)

  def test_syo_edullisesti_kateisella_nostaa_myytyjen_lounaiden_maaraa_oikein(self):
    self.kassapaate.syo_edullisesti_kateisella(300)

    self.assertEqual(self.kassapaate.edulliset, 1)

  def test_syo_edullisesti_kateisella_kasvattaa_kassaa_oikein(self):
    self.kassapaate.syo_edullisesti_kateisella(300)

    self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.40)

  def test_syo_edullisesti_palauttaa_kaikki_jos_raha_ei_riita(self):
    self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)

  def test_syo_edullisesti_ei_muuta_lounaiden_maaraa_jos_raha_ei_riita(self):
    self.kassapaate.syo_edullisesti_kateisella(100)

    self.assertEqual(self.kassapaate.edulliset, 0)

  def test_syo_maukkaasti_kateisella_palauttaa_vaihtorahat_oikein(self):
    self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)

  def test_syo_maukkaasti_kateisella_nostaa_myytyjen_lounaiden_maaraa_oikein(self):
    self.kassapaate.syo_maukkaasti_kateisella(500)

    self.assertEqual(self.kassapaate.maukkaat, 1)

  def test_syo_maukkaasti_kateisella_kasvattaa_kassaa_oikein(self):
    self.kassapaate.syo_maukkaasti_kateisella(600)

    self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.00)

  def test_syo_maukkaasti_palauttaa_kaikki_jos_raha_ei_riita(self):
    self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(200), 200)

  def test_syo_maukkaasti_ei_muuta_lounaiden_maaraa_jos_raha_ei_riita(self):
    self.kassapaate.syo_maukkaasti_kateisella(100)

    self.assertEqual(self.kassapaate.maukkaat, 0)

  def test_syo_edullisesti_kortilla_ei_muuta_kassassa_olevaa_summaa(self):
    self.kassapaate.syo_edullisesti_kortilla(self.kortti)

    self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

  def test_syo_maukkaasti_kortilla_ei_muuta_kassassa_olevaa_summaa(self):
    self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

    self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

  def test_syo_edullisesti_kortilla_toimii_oikein_kun_raha_riittaa(self):
    self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), True)
    self.assertEqual(self.kortti.saldo_euroina(), 7.60)

  def test_syo_maukkaasti_kortilla_toimii_oikein_kun_raha_riittaa(self):
    self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), True)
    self.assertEqual(self.kortti.saldo_euroina(), 6.00)

  def test_syo_edullisesti_kortilla_kasvattaa_myytyjen_lounaiden_maaraa(self):
    self.kassapaate.syo_edullisesti_kortilla(self.kortti)

    self.assertEqual(self.kassapaate.edulliset, 1)

  def test_syo_maukkaasti_kortilla_kasvattaa_myytyjen_lounaiden_maaraa(self):
    self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

    self.assertEqual(self.kassapaate.maukkaat, 1)

  def test_syo_edullisesti_kortilla_palauttaa_false_eika_muuta_mitaan_kun_raha_ei_riita(self):
    kortti = Maksukortti(100)
    self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), False)

    self.assertEqual(self.kassapaate.edulliset, 0)
    self.assertEqual(kortti.saldo_euroina(), 1.00)

  def test_syo_maukkaasti_kortilla_palauttaa_false_eika_muuta_mitaan_kun_raha_ei_riita(self):
    kortti = Maksukortti(100)
    self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), False)

    self.assertEqual(self.kassapaate.maukkaat, 0)
    self.assertEqual(kortti.saldo_euroina(), 1.00)

  def test_lataa_rahaa_kortille_kasvattaa_kassan_ja_kortin_saldoa_oikein(self):
    self.kassapaate.lataa_rahaa_kortille(self.kortti, 1000)

    self.assertEqual(self.kortti.saldo_euroina(), 20)
    self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1010.00)

  def test_lataa_rahaa_kortille_ei_muuta_kassan_ja_kortin_saldoa_jos_summa_on_negatiivinen(self):
    self.kassapaate.lataa_rahaa_kortille(self.kortti, -1000)

    self.assertEqual(self.kortti.saldo_euroina(), 10)
    self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)
