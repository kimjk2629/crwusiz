from openpilot.selfdrive.car.interfaces import get_interface_attr
from openpilot.selfdrive.car.body.values import CAR as BODY
from openpilot.selfdrive.car.chrysler.values import CAR as CHRYSLER
from openpilot.selfdrive.car.ford.values import CAR as FORD
from openpilot.selfdrive.car.gm.values import CAR as GM
from openpilot.selfdrive.car.honda.values import CAR as HONDA
from openpilot.selfdrive.car.hyundai.values import CAR as HYUNDAI
from openpilot.selfdrive.car.mazda.values import CAR as MAZDA
from openpilot.selfdrive.car.mock.values import CAR as MOCK
from openpilot.selfdrive.car.nissan.values import CAR as NISSAN
from openpilot.selfdrive.car.subaru.values import CAR as SUBARU
from openpilot.selfdrive.car.tesla.values import CAR as TESLA
from openpilot.selfdrive.car.toyota.values import CAR as TOYOTA
from openpilot.selfdrive.car.volkswagen.values import CAR as VW

FW_VERSIONS = get_interface_attr('FW_VERSIONS', combine_brands=True, ignore_none=True)
_FINGERPRINTS = get_interface_attr('FINGERPRINTS', combine_brands=True, ignore_none=True)

_DEBUG_ADDRESS = {1880: 8}   # reserved for debug purposes


def is_valid_for_fingerprint(msg, car_fingerprint: dict[int, int]):
  adr = msg.address
  # ignore addresses that are more than 11 bits
  return (adr in car_fingerprint and car_fingerprint[adr] == len(msg.dat)) or adr >= 0x800


def eliminate_incompatible_cars(msg, candidate_cars):
  """Removes cars that could not have sent msg.

     Inputs:
      msg: A cereal/log CanData message from the car.
      candidate_cars: A list of cars to consider.

     Returns:
      A list containing the subset of candidate_cars that could have sent msg.
  """
  compatible_cars = []

  for car_name in candidate_cars:
    car_fingerprints = _FINGERPRINTS[car_name]

    for fingerprint in car_fingerprints:
      # add alien debug address
      if is_valid_for_fingerprint(msg, fingerprint | _DEBUG_ADDRESS):
        compatible_cars.append(car_name)
        break

  return compatible_cars


def all_known_cars():
  """Returns a list of all known car strings."""
  return list({*FW_VERSIONS.keys(), *_FINGERPRINTS.keys()})


def all_legacy_fingerprint_cars():
  """Returns a list of all known car strings, FPv1 only."""
  return list(_FINGERPRINTS.keys())


# A dict that maps old platform strings to their latest representations
MIGRATION = {
  "ACURA ILX 2016 ACURAWATCH PLUS": HONDA.ACURA_ILX,
  "ACURA RDX 2018 ACURAWATCH PLUS": HONDA.ACURA_RDX,
  "ACURA RDX 2020 TECH": HONDA.ACURA_RDX_3G,
  "AUDI A3": VW.AUDI_A3_MK3,
  "HONDA ACCORD 2018 HYBRID TOURING": HONDA.HONDA_ACCORD,
  "HONDA ACCORD 1.5T 2018": HONDA.HONDA_ACCORD,
  "HONDA ACCORD 2018 LX 1.5T": HONDA.HONDA_ACCORD,
  "HONDA ACCORD 2018 SPORT 2T": HONDA.HONDA_ACCORD,
  "HONDA ACCORD 2T 2018": HONDA.HONDA_ACCORD,
  "HONDA ACCORD HYBRID 2018": HONDA.HONDA_ACCORD,
  "HONDA CIVIC 2016 TOURING": HONDA.HONDA_CIVIC,
  "HONDA CIVIC HATCHBACK 2017 SEDAN/COUPE 2019": HONDA.HONDA_CIVIC_BOSCH,
  "HONDA CIVIC SEDAN 1.6 DIESEL": HONDA.HONDA_CIVIC_BOSCH_DIESEL,
  "HONDA CR-V 2016 EXECUTIVE": HONDA.HONDA_CRV_EU,
  "HONDA CR-V 2016 TOURING": HONDA.HONDA_CRV,
  "HONDA CR-V 2017 EX": HONDA.HONDA_CRV_5G,
  "HONDA CR-V 2019 HYBRID": HONDA.HONDA_CRV_HYBRID,
  "HONDA FIT 2018 EX": HONDA.HONDA_FIT,
  "HONDA HRV 2019 TOURING": HONDA.HONDA_HRV,
  "HONDA INSIGHT 2019 TOURING": HONDA.HONDA_INSIGHT,
  "HONDA ODYSSEY 2018 EX-L": HONDA.HONDA_ODYSSEY,
  "HONDA ODYSSEY 2019 EXCLUSIVE CHN": HONDA.HONDA_ODYSSEY_CHN,
  "HONDA PILOT 2017 TOURING": HONDA.HONDA_PILOT,
  "HONDA PILOT 2019 ELITE": HONDA.HONDA_PILOT,
  "HONDA PILOT 2019": HONDA.HONDA_PILOT,
  "HONDA PASSPORT 2021": HONDA.HONDA_PILOT,
  "HONDA RIDGELINE 2017 BLACK EDITION": HONDA.HONDA_RIDGELINE,
  "LEXUS CT 200H 2018": TOYOTA.LEXUS_CTH,
  "LEXUS ES 300H 2018": TOYOTA.LEXUS_ES,
  "LEXUS ES 300H 2019": TOYOTA.LEXUS_ES_TSS2,
  "LEXUS IS300 2018": TOYOTA.LEXUS_IS,
  "LEXUS NX300 2018": TOYOTA.LEXUS_NX,
  "LEXUS NX300H 2018": TOYOTA.LEXUS_NX,
  "LEXUS RX 350 2016": TOYOTA.LEXUS_RX,
  "LEXUS RX350 2020": TOYOTA.LEXUS_RX_TSS2,
  "LEXUS RX450 HYBRID 2020": TOYOTA.LEXUS_RX_TSS2,
  "TOYOTA SIENNA XLE 2018": TOYOTA.TOYOTA_SIENNA,
  "TOYOTA C-HR HYBRID 2018": TOYOTA.TOYOTA_CHR,
  "TOYOTA COROLLA HYBRID TSS2 2019": TOYOTA.TOYOTA_COROLLA_TSS2,
  "TOYOTA RAV4 HYBRID 2019": TOYOTA.TOYOTA_RAV4_TSS2,
  "LEXUS ES HYBRID 2019": TOYOTA.LEXUS_ES_TSS2,
  "LEXUS NX HYBRID 2018": TOYOTA.LEXUS_NX,
  "LEXUS NX HYBRID 2020": TOYOTA.LEXUS_NX_TSS2,
  "LEXUS RX HYBRID 2020": TOYOTA.LEXUS_RX_TSS2,
  "TOYOTA ALPHARD HYBRID 2021": TOYOTA.TOYOTA_ALPHARD_TSS2,
  "TOYOTA AVALON HYBRID 2019": TOYOTA.TOYOTA_AVALON_2019,
  "TOYOTA AVALON HYBRID 2022": TOYOTA.TOYOTA_AVALON_TSS2,
  "TOYOTA CAMRY HYBRID 2018": TOYOTA.TOYOTA_CAMRY,
  "TOYOTA CAMRY HYBRID 2021": TOYOTA.TOYOTA_CAMRY_TSS2,
  "TOYOTA C-HR HYBRID 2022": TOYOTA.TOYOTA_CHR_TSS2,
  "TOYOTA HIGHLANDER HYBRID 2020": TOYOTA.TOYOTA_HIGHLANDER_TSS2,
  "TOYOTA RAV4 HYBRID 2022": TOYOTA.TOYOTA_RAV4_TSS2_2022,
  "TOYOTA RAV4 HYBRID 2023": TOYOTA.TOYOTA_RAV4_TSS2_2023,
  "TOYOTA HIGHLANDER HYBRID 2018": TOYOTA.TOYOTA_HIGHLANDER,
  "LEXUS ES HYBRID 2018": TOYOTA.LEXUS_ES,
  "LEXUS RX HYBRID 2017": TOYOTA.LEXUS_RX,

  # Removal of platform_str, see https://github.com/commaai/openpilot/pull/31868/
  "COMMA BODY": BODY.COMMA_BODY,
  "CHRYSLER PACIFICA HYBRID 2017": CHRYSLER.CHRYSLER_PACIFICA_2017_HYBRID,
  "CHRYSLER PACIFICA HYBRID 2018": CHRYSLER.CHRYSLER_PACIFICA_2018_HYBRID,
  "CHRYSLER PACIFICA HYBRID 2019": CHRYSLER.CHRYSLER_PACIFICA_2019_HYBRID,
  "CHRYSLER PACIFICA 2018": CHRYSLER.CHRYSLER_PACIFICA_2018,
  "CHRYSLER PACIFICA 2020": CHRYSLER.CHRYSLER_PACIFICA_2020,
  "DODGE DURANGO 2021": CHRYSLER.DODGE_DURANGO,
  "JEEP GRAND CHEROKEE V6 2018": CHRYSLER.JEEP_GRAND_CHEROKEE,
  "JEEP GRAND CHEROKEE 2019": CHRYSLER.JEEP_GRAND_CHEROKEE_2019,
  "RAM 1500 5TH GEN": CHRYSLER.RAM_1500_5TH_GEN,
  "RAM HD 5TH GEN": CHRYSLER.RAM_HD_5TH_GEN,
  "FORD BRONCO SPORT 1ST GEN": FORD.FORD_BRONCO_SPORT_MK1,
  "FORD ESCAPE 4TH GEN": FORD.FORD_ESCAPE_MK4,
  "FORD EXPLORER 6TH GEN": FORD.FORD_EXPLORER_MK6,
  "FORD F-150 14TH GEN": FORD.FORD_F_150_MK14,
  "FORD F-150 LIGHTNING 1ST GEN": FORD.FORD_F_150_LIGHTNING_MK1,
  "FORD FOCUS 4TH GEN": FORD.FORD_FOCUS_MK4,
  "FORD MAVERICK 1ST GEN": FORD.FORD_MAVERICK_MK1,
  "FORD MUSTANG MACH-E 1ST GEN": FORD.FORD_MUSTANG_MACH_E_MK1,
  "HOLDEN ASTRA RS-V BK 2017": GM.HOLDEN_ASTRA,
  "CHEVROLET VOLT PREMIER 2017": GM.CHEVROLET_VOLT,
  "CADILLAC ATS Premium Performance 2018": GM.CADILLAC_ATS,
  "CHEVROLET MALIBU PREMIER 2017": GM.CHEVROLET_MALIBU,
  "GMC ACADIA DENALI 2018": GM.GMC_ACADIA,
  "BUICK LACROSSE 2017": GM.BUICK_LACROSSE,
  "BUICK REGAL ESSENCE 2018": GM.BUICK_REGAL,
  "CADILLAC ESCALADE 2017": GM.CADILLAC_ESCALADE,
  "CADILLAC ESCALADE ESV 2016": GM.CADILLAC_ESCALADE_ESV,
  "CADILLAC ESCALADE ESV 2019": GM.CADILLAC_ESCALADE_ESV_2019,
  "CHEVROLET BOLT EUV 2022": GM.CHEVROLET_BOLT_EUV,
  "CHEVROLET SILVERADO 1500 2020": GM.CHEVROLET_SILVERADO,
  "CHEVROLET EQUINOX 2019": GM.CHEVROLET_EQUINOX,
  "CHEVROLET TRAILBLAZER 2021": GM.CHEVROLET_TRAILBLAZER,
  "HONDA ACCORD 2018": HONDA.HONDA_ACCORD,
  "HONDA CIVIC (BOSCH) 2019": HONDA.HONDA_CIVIC_BOSCH,
  "HONDA CIVIC SEDAN 1.6 DIESEL 2019": HONDA.HONDA_CIVIC_BOSCH_DIESEL,
  "HONDA CIVIC 2022": HONDA.HONDA_CIVIC_2022,
  "HONDA CR-V 2017": HONDA.HONDA_CRV_5G,
  "HONDA CR-V HYBRID 2019": HONDA.HONDA_CRV_HYBRID,
  "HONDA HR-V 2023": HONDA.HONDA_HRV_3G,
  "ACURA RDX 2020": HONDA.ACURA_RDX_3G,
  "HONDA INSIGHT 2019": HONDA.HONDA_INSIGHT,
  "HONDA E 2020": HONDA.HONDA_E,
  "ACURA ILX 2016": HONDA.ACURA_ILX,
  "HONDA CR-V 2016": HONDA.HONDA_CRV,
  "HONDA CR-V EU 2016": HONDA.HONDA_CRV_EU,
  "HONDA FIT 2018": HONDA.HONDA_FIT,
  "HONDA FREED 2020": HONDA.HONDA_FREED,
  "HONDA HRV 2019": HONDA.HONDA_HRV,
  "HONDA ODYSSEY 2018": HONDA.HONDA_ODYSSEY,
  "HONDA ODYSSEY CHN 2019": HONDA.HONDA_ODYSSEY_CHN,
  "ACURA RDX 2018": HONDA.ACURA_RDX,
  "HONDA PILOT 2017": HONDA.HONDA_PILOT,
  "HONDA RIDGELINE 2017": HONDA.HONDA_RIDGELINE,
  "HONDA CIVIC 2016": HONDA.HONDA_CIVIC,
  "MAZDA CX-5": MAZDA.MAZDA_CX5,
  "MAZDA CX-9": MAZDA.MAZDA_CX9,
  "MAZDA 3": MAZDA.MAZDA_3,
  "MAZDA 6": MAZDA.MAZDA_6,
  "MAZDA CX-9 2021": MAZDA.MAZDA_CX9_2021,
  "MAZDA CX-5 2022": MAZDA.MAZDA_CX5_2022,
  "NISSAN X-TRAIL 2017": NISSAN.NISSAN_XTRAIL,
  "NISSAN LEAF 2018": NISSAN.NISSAN_LEAF,
  "NISSAN LEAF 2018 Instrument Cluster": NISSAN.NISSAN_LEAF_IC,
  "NISSAN ROGUE 2019": NISSAN.NISSAN_ROGUE,
  "NISSAN ALTIMA 2020": NISSAN.NISSAN_ALTIMA,
  "SUBARU ASCENT LIMITED 2019": SUBARU.SUBARU_ASCENT,
  "SUBARU OUTBACK 6TH GEN": SUBARU.SUBARU_OUTBACK,
  "SUBARU LEGACY 7TH GEN": SUBARU.SUBARU_LEGACY,
  "SUBARU IMPREZA LIMITED 2019": SUBARU.SUBARU_IMPREZA,
  "SUBARU IMPREZA SPORT 2020": SUBARU.SUBARU_IMPREZA_2020,
  "SUBARU CROSSTREK HYBRID 2020": SUBARU.SUBARU_CROSSTREK_HYBRID,
  "SUBARU FORESTER 2019": SUBARU.SUBARU_FORESTER,
  "SUBARU FORESTER HYBRID 2020": SUBARU.SUBARU_FORESTER_HYBRID,
  "SUBARU FORESTER 2017 - 2018": SUBARU.SUBARU_FORESTER_PREGLOBAL,
  "SUBARU LEGACY 2015 - 2018": SUBARU.SUBARU_LEGACY_PREGLOBAL,
  "SUBARU OUTBACK 2015 - 2017": SUBARU.SUBARU_OUTBACK_PREGLOBAL,
  "SUBARU OUTBACK 2018 - 2019": SUBARU.SUBARU_OUTBACK_PREGLOBAL_2018,
  "SUBARU FORESTER 2022": SUBARU.SUBARU_FORESTER_2022,
  "SUBARU OUTBACK 7TH GEN": SUBARU.SUBARU_OUTBACK_2023,
  "SUBARU ASCENT 2023": SUBARU.SUBARU_ASCENT_2023,
  'TESLA AP1 MODEL S': TESLA.TESLA_AP1_MODELS,
  'TESLA AP2 MODEL S': TESLA.TESLA_AP2_MODELS,
  'TESLA MODEL S RAVEN': TESLA.TESLA_MODELS_RAVEN,
  "TOYOTA ALPHARD 2020": TOYOTA.TOYOTA_ALPHARD_TSS2,
  "TOYOTA AVALON 2016": TOYOTA.TOYOTA_AVALON,
  "TOYOTA AVALON 2019": TOYOTA.TOYOTA_AVALON_2019,
  "TOYOTA AVALON 2022": TOYOTA.TOYOTA_AVALON_TSS2,
  "TOYOTA CAMRY 2018": TOYOTA.TOYOTA_CAMRY,
  "TOYOTA CAMRY 2021": TOYOTA.TOYOTA_CAMRY_TSS2,
  "TOYOTA C-HR 2018": TOYOTA.TOYOTA_CHR,
  "TOYOTA C-HR 2021": TOYOTA.TOYOTA_CHR_TSS2,
  "TOYOTA COROLLA 2017": TOYOTA.TOYOTA_COROLLA,
  "TOYOTA COROLLA TSS2 2019": TOYOTA.TOYOTA_COROLLA_TSS2,
  "TOYOTA HIGHLANDER 2017": TOYOTA.TOYOTA_HIGHLANDER,
  "TOYOTA HIGHLANDER 2020": TOYOTA.TOYOTA_HIGHLANDER_TSS2,
  "TOYOTA PRIUS 2017": TOYOTA.TOYOTA_PRIUS,
  "TOYOTA PRIUS v 2017": TOYOTA.TOYOTA_PRIUS_V,
  "TOYOTA PRIUS TSS2 2021": TOYOTA.TOYOTA_PRIUS_TSS2,
  "TOYOTA RAV4 2017": TOYOTA.TOYOTA_RAV4,
  "TOYOTA RAV4 HYBRID 2017": TOYOTA.TOYOTA_RAV4H,
  "TOYOTA RAV4 2019": TOYOTA.TOYOTA_RAV4_TSS2,
  "TOYOTA RAV4 2022": TOYOTA.TOYOTA_RAV4_TSS2_2022,
  "TOYOTA RAV4 2023": TOYOTA.TOYOTA_RAV4_TSS2_2023,
  "TOYOTA MIRAI 2021": TOYOTA.TOYOTA_MIRAI,
  "TOYOTA SIENNA 2018": TOYOTA.TOYOTA_SIENNA,
  "LEXUS CT HYBRID 2018": TOYOTA.LEXUS_CTH,
  "LEXUS ES 2018": TOYOTA.LEXUS_ES,
  "LEXUS ES 2019": TOYOTA.LEXUS_ES_TSS2,
  "LEXUS IS 2018": TOYOTA.LEXUS_IS,
  "LEXUS IS 2023": TOYOTA.LEXUS_IS_TSS2,
  "LEXUS NX 2018": TOYOTA.LEXUS_NX,
  "LEXUS NX 2020": TOYOTA.LEXUS_NX_TSS2,
  "LEXUS LC 2024": TOYOTA.LEXUS_LC_TSS2,
  "LEXUS RC 2020": TOYOTA.LEXUS_RC,
  "LEXUS RX 2016": TOYOTA.LEXUS_RX,
  "LEXUS RX 2020": TOYOTA.LEXUS_RX_TSS2,
  "LEXUS GS F 2016": TOYOTA.LEXUS_GS_F,
  "VOLKSWAGEN ARTEON 1ST GEN": VW.VOLKSWAGEN_ARTEON_MK1,
  "VOLKSWAGEN ATLAS 1ST GEN": VW.VOLKSWAGEN_ATLAS_MK1,
  "VOLKSWAGEN CADDY 3RD GEN": VW.VOLKSWAGEN_CADDY_MK3,
  "VOLKSWAGEN CRAFTER 2ND GEN": VW.VOLKSWAGEN_CRAFTER_MK2,
  "VOLKSWAGEN GOLF 7TH GEN": VW.VOLKSWAGEN_GOLF_MK7,
  "VOLKSWAGEN JETTA 7TH GEN": VW.VOLKSWAGEN_JETTA_MK7,
  "VOLKSWAGEN PASSAT 8TH GEN": VW.VOLKSWAGEN_PASSAT_MK8,
  "VOLKSWAGEN PASSAT NMS": VW.VOLKSWAGEN_PASSAT_NMS,
  "VOLKSWAGEN POLO 6TH GEN": VW.VOLKSWAGEN_POLO_MK6,
  "VOLKSWAGEN SHARAN 2ND GEN": VW.VOLKSWAGEN_SHARAN_MK2,
  "VOLKSWAGEN TAOS 1ST GEN": VW.VOLKSWAGEN_TAOS_MK1,
  "VOLKSWAGEN T-CROSS 1ST GEN": VW.VOLKSWAGEN_TCROSS_MK1,
  "VOLKSWAGEN TIGUAN 2ND GEN": VW.VOLKSWAGEN_TIGUAN_MK2,
  "VOLKSWAGEN TOURAN 2ND GEN": VW.VOLKSWAGEN_TOURAN_MK2,
  "VOLKSWAGEN TRANSPORTER T6.1": VW.VOLKSWAGEN_TRANSPORTER_T61,
  "VOLKSWAGEN T-ROC 1ST GEN": VW.VOLKSWAGEN_TROC_MK1,
  "AUDI A3 3RD GEN": VW.AUDI_A3_MK3,
  "AUDI Q2 1ST GEN": VW.AUDI_Q2_MK1,
  "AUDI Q3 2ND GEN": VW.AUDI_Q3_MK2,
  "SEAT ATECA 1ST GEN": VW.SEAT_ATECA_MK1,
  "SEAT LEON 3RD GEN": VW.SEAT_ATECA_MK1,
  "SEAT_LEON_MK3": VW.SEAT_ATECA_MK1,
  "SKODA FABIA 4TH GEN": VW.SKODA_FABIA_MK4,
  "SKODA KAMIQ 1ST GEN": VW.SKODA_KAMIQ_MK1,
  "SKODA KAROQ 1ST GEN": VW.SKODA_KAROQ_MK1,
  "SKODA KODIAQ 1ST GEN": VW.SKODA_KODIAQ_MK1,
  "SKODA OCTAVIA 3RD GEN": VW.SKODA_OCTAVIA_MK3,
  "SKODA SCALA 1ST GEN": VW.SKODA_KAMIQ_MK1,
  "SKODA_SCALA_MK1": VW.SKODA_KAMIQ_MK1,
  "SKODA SUPERB 3RD GEN": VW.SKODA_SUPERB_MK3,

  "HYUNDAI AVANTE (AD)": HYUNDAI.HYUNDAI_AVANTE,
  "HYUNDAI I30 (PD)": HYUNDAI.HYUNDAI_I30,
  "HYUNDAI AVANTE (CN7)": HYUNDAI.HYUNDAI_AVANTE_CN7,
  "HYUNDAI AVANTE HYBRID (CN7)": HYUNDAI.HYUNDAI_AVANTE_CN7_HEV,
  "HYUNDAI SONATA (LF)": HYUNDAI.HYUNDAI_SONATA_LF,
  "HYUNDAI SONATA HYBRID (LF)": HYUNDAI.HYUNDAI_SONATA_LF_HEV,
  "HYUNDAI SONATA (DN8)": HYUNDAI.HYUNDAI_SONATA_DN8,
  "HYUNDAI SONATA HYBRID (DN8)": HYUNDAI.HYUNDAI_SONATA_DN8_HEV,
  "HYUNDAI KONA (OS)": HYUNDAI.HYUNDAI_KONA,
  "HYUNDAI KONA EV (OS)": HYUNDAI.HYUNDAI_KONA_EV,
  "HYUNDAI KONA HYBRID (OS)": HYUNDAI.HYUNDAI_KONA_HEV,
  "HYUNDAI IONIQ (AE)": HYUNDAI.HYUNDAI_IONIQ,
  "HYUNDAI IONIQ EV (AE)": HYUNDAI.HYUNDAI_IONIQ_EV,
  "HYUNDAI IONIQ HYBRID (AE)": HYUNDAI.HYUNDAI_IONIQ_HEV,
  "HYUNDAI TUCSON (TL)": HYUNDAI.HYUNDAI_TUCSON,
  "HYUNDAI SANTAFE (TM)": HYUNDAI.HYUNDAI_SANTAFE,
  "HYUNDAI SANTAFE HYBRID (TM)": HYUNDAI.HYUNDAI_SANTAFE_HEV,
  "HYUNDAI PALISADE (LX2)": HYUNDAI.HYUNDAI_PALISADE,
  "HYUNDAI VELOSTER (JS)": HYUNDAI.HYUNDAI_VELOSTER,
  "HYUNDAI GRANDEUR (IG)": HYUNDAI.HYUNDAI_GRANDEUR,
  "HYUNDAI GRANDEUR HYBRID (IG)": HYUNDAI.HYUNDAI_GRANDEUR_HEV,
  "HYUNDAI GRANDEUR FL (IG)": HYUNDAI.HYUNDAI_GRANDEUR_FL,
  "HYUNDAI GRANDEUR FL HYBRID (IG)": HYUNDAI.HYUNDAI_GRANDEUR_FL_HEV,
  "HYUNDAI NEXO (FE)": HYUNDAI.HYUNDAI_NEXO,
  "HYUNDAI SONATA_2024 (DN8)": HYUNDAI.HYUNDAI_SONATA_DN8_24,
  "HYUNDAI KONA EV (SX2)": HYUNDAI.HYUNDAI_KONA_SX2_EV,
  "HYUNDAI IONIQ 5 (NE1)": HYUNDAI.HYUNDAI_IONIQ5,
  "HYUNDAI IONIQ 6 (CE1)": HYUNDAI.HYUNDAI_IONIQ6,
  "HYUNDAI TUCSON (NX4)": HYUNDAI.HYUNDAI_TUCSON_NX4,
  "HYUNDAI TUCSON HYBRID (NX4)": HYUNDAI.HYUNDAI_TUCSON_NX4_HEV,
  "HYUNDAI STARIA (US4)": HYUNDAI.HYUNDAI_STARIA,

  "KIA K3 (BD)": HYUNDAI.KIA_K3,
  "KIA K5 (JF)": HYUNDAI.KIA_K5,
  "KIA K5 HYBRID (JF)": HYUNDAI.KIA_K5_HEV,
  "KIA K5 (DL3)": HYUNDAI.KIA_K5_DL3,
  "KIA K5 HYBRID (DL3)": HYUNDAI.KIA_K5_DL3_HEV,
  "KIA K7 (YG)": HYUNDAI.KIA_K7,
  "KIA K7 HYBRID (YG)": HYUNDAI.KIA_K7_HEV,
  "KIA K9 (RJ)": HYUNDAI.KIA_K9,
  "KIA SPORTAGE (QL)": HYUNDAI.KIA_SPORTAGE,
  "KIA SORENTO (UM)": HYUNDAI.KIA_SORENTO,
  "KIA MOHAVE (HM)": HYUNDAI.KIA_MOHAVE,
  "KIA STINGER (CK)": HYUNDAI.KIA_STINGER,
  "KIA NIRO EV (DE)": HYUNDAI.KIA_NIRO_EV,
  "KIA NIRO HYBRID (DE)": HYUNDAI.KIA_NIRO_HEV,
  "KIA SOUL EV (SK3)": HYUNDAI.KIA_SOUL_EV,
  "KIA SELTOS (SP2)": HYUNDAI.KIA_SELTOS,
  "KIA EV6 (CV1)": HYUNDAI.KIA_EV6,
  "KIA K5 2024 (DL3)": HYUNDAI.KIA_K5_DL3_24,
  "KIA K5 HYBRID 2024 (DL3)": HYUNDAI.KIA_K5_DL3_24_HEV,
  "KIA K8 (GL3)": HYUNDAI.KIA_K8_GL3,
  "KIA K8 HYBRID (GL3)": HYUNDAI.KIA_K8_GL3_HEV,
  "KIA SPORTAGE (NQ5)": HYUNDAI.KIA_SPORTAGE_NQ5,
  "KIA SPORTAGE HYBRID (NQ5)": HYUNDAI.KIA_SPORTAGE_NQ5_HEV,
  "KIA SORENTO (MQ4)": HYUNDAI.KIA_SORENTO_MQ4,
  "KIA SORENTO HYBRID (MQ4)": HYUNDAI.KIA_SORENTO_MQ4_HEV,
  "KIA NIRO EV (SG2)": HYUNDAI.KIA_NIRO_SG2_EV,
  "KIA NIRO HYBRID (SG2)": HYUNDAI.KIA_NIRO_SG2_HEV,
  "KIA EV9 (MV)": HYUNDAI.KIA_EV9,

  "GENESIS (DH)": HYUNDAI.GENESIS,
  "GENESIS G70 (IK)": HYUNDAI.GENESIS_G70,
  "GENESIS G80 (DH)": HYUNDAI.GENESIS_G80,
  "GENESIS G90 (HI)": HYUNDAI.GENESIS_G90,
  "GENESIS GV60 (JW1)": HYUNDAI.GENESIS_GV60,
  "GENESIS GV70 (JK1)": HYUNDAI.GENESIS_GV70,
  "GENESIS GV80 (JX1)": HYUNDAI.GENESIS_GV80,

  "mock": MOCK.MOCK,
}


def extract_platform(info: str) -> str:
  platform_name = MIGRATION[info].split(".")[-1]
  return platform_name