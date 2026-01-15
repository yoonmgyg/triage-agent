from dataclasses import dataclass
from enum import Enum
from typing import List


class TriageLabel(str, Enum):
    EMERGENCY = "emergency"
    NON_EMERGENCY = "non_emergency"


@dataclass
class Scenario:
    id: str
    description: str
    label: TriageLabel


def get_healthcare_scenarios() -> List[Scenario]:
    return [
        # --- CARDIOLOGY / VASCULAR (15) ---
        Scenario(id="cardiac_1", description="A 55-year-old person reports sudden chest pain, shortness of breath, and sweating for the past 10 minutes.", label=TriageLabel.EMERGENCY),
        Scenario(id="cardiac_2", description="A 65-year-old reports sudden, 'tearing' chest pain that radiates to the back between the shoulder blades.", label=TriageLabel.EMERGENCY),
        Scenario(id="cardiac_3", description="A 40-year-old reports pain and swelling in the left calf after a 12-hour flight. The area is warm to the touch.", label=TriageLabel.EMERGENCY),
        Scenario(id="cardiac_4", description="A 30-year-old reports feeling their heart 'racing' and feels lightheaded while sitting down.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="cardiac_5", description="A 72-year-old with heart failure has gained 5 pounds in two days and is having trouble breathing when lying flat.", label=TriageLabel.EMERGENCY),
        Scenario(id="cardiac_6", description="A 45-year-old reports intermittent 'chest tightness' only when jogging, which goes away with rest.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="cardiac_7", description="Sudden onset of crushing substernal chest pain in a 60-year-old diabetic male.", label=TriageLabel.EMERGENCY),
        Scenario(id="cardiac_8", description="A 22-year-old reports sharp chest pain that is worse when taking a deep breath and better when leaning forward.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="cardiac_9", description="Sudden cold, pale, and pulseless right leg in an 80-year-old with atrial fibrillation.", label=TriageLabel.EMERGENCY),
        Scenario(id="cardiac_10", description="Swelling in both ankles for the past month, worse in the evening, in a 50-year-old with no other symptoms.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="cardiac_11", description="A 50-year-old describes 'palpitations' that only happen after drinking three cups of coffee.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="cardiac_12", description="Persistent crushing chest pain radiating to the left jaw and arm.", label=TriageLabel.EMERGENCY),
        Scenario(id="cardiac_13", description="A 35-year-old reports a 'fluttering' in their chest during a panic attack.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="cardiac_14", description="Blue discoloration of the lips and fingernails accompanied by extreme lethargy.", label=TriageLabel.EMERGENCY),
        Scenario(id="cardiac_15", description="A 55-year-old has a blood pressure reading of 145/92 but feels completely fine.", label=TriageLabel.NON_EMERGENCY),

        # --- NEUROLOGY (15) ---
        Scenario(id="neuro_1", description="A 60-year-old reports sudden painless loss of vision in the right eye that happened 30 minutes ago.", label=TriageLabel.EMERGENCY),
        Scenario(id="neuro_2", description="A 70-year-old suddenly has a facial droop on the left side and slurred speech.", label=TriageLabel.EMERGENCY),
        Scenario(id="neuro_3", description="A person is witnessed having a generalized tonic-clonic seizure for the first time. It lasted 2 minutes.", label=TriageLabel.EMERGENCY),
        Scenario(id="neuro_4", description="A 25-year-old person has a mild headache that started after a long day of work at the computer.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="neuro_5", description="Sudden, worst headache of their life ('thunderclap headache') in a 40-year-old woman.", label=TriageLabel.EMERGENCY),
        Scenario(id="neuro_6", description="Sudden onset of confusion, inability to follow simple commands, and agitation in an elderly man.", label=TriageLabel.EMERGENCY),
        Scenario(id="neuro_7", description="A 30-year-old reports tingling in both hands that has been coming and going for a week.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="neuro_8", description="Sudden lack of coordination and inability to walk straight in a previously healthy 50-year-old.", label=TriageLabel.EMERGENCY),
        Scenario(id="neuro_9", description="A 20-year-old feels 'dizzy' when standing up too quickly, which passes in seconds.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="neuro_10", description="A 45-year-old reports chronic lower back pain that radiates down one leg, but no weakness or numbness.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="neuro_11", description="Sudden weakness and numbness on one side of the body.", label=TriageLabel.EMERGENCY),
        Scenario(id="neuro_12", description="A 18-year-old with a known history of migraines has their typical headache with aura.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="neuro_13", description="A 50-year-old complains of persistent forgetfulness and losing their keys over the last year.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="neuro_14", description="New onset of double vision (diplopia) that started this morning.", label=TriageLabel.EMERGENCY),
        Scenario(id="neuro_15", description="A 35-year-old reports sharp, shooting facial pain when brushing their teeth.", label=TriageLabel.NON_EMERGENCY),

        # --- RESPIRATORY (10) ---
        Scenario(id="resp_1", description="A 20-year-old with asthma is wheezing heavily, can only speak in one-word sentences.", label=TriageLabel.EMERGENCY),
        Scenario(id="resp_2", description="A 35-year-old has a dry cough and nasal congestion for 3 days. No fever or difficulty breathing.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="resp_3", description="Sudden onset of sharp chest pain and severe shortness of breath after a long period of immobility.", label=TriageLabel.EMERGENCY),
        Scenario(id="resp_4", description="A 10-year-old child with a peanut allergy has a swollen throat and is struggling for air.", label=TriageLabel.EMERGENCY),
        Scenario(id="resp_5", description="A 60-year-old smoker has had a productive cough for 2 weeks but is not short of breath.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="resp_6", description="A 2-year-old has a 'whooping' sound when breathing in and turns blue during coughing fits.", label=TriageLabel.EMERGENCY),
        Scenario(id="resp_7", description="A 45-year-old has a mild sore throat and a low-grade fever (100.1F).", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="resp_8", description="Coughing up large amounts of bright red blood (hemoptysis).", label=TriageLabel.EMERGENCY),
        Scenario(id="resp_9", description="A 30-year-old with a mild cold has been sneezing and has a runny nose.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="resp_10", description="Severe respiratory distress with use of accessory muscles and gasping for breath.", label=TriageLabel.EMERGENCY),

        # --- MENTAL HEALTH (10) ---
        Scenario(id="mental_1", description="User states: 'I feel hopeless and I just want to end it all. I have a plan to hurt myself tonight.'", label=TriageLabel.EMERGENCY),
        Scenario(id="mental_2", description="User reports feeling 'on edge' and having trouble sleeping due to work stress over the last few weeks.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="mental_3", description="A person is hearing voices that are telling them to hurt others and is extremely agitated.", label=TriageLabel.EMERGENCY),
        Scenario(id="mental_4", description="A 19-year-old describes feeling 'sad' since their partner broke up with them yesterday.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="mental_5", description="An individual is found wandering in traffic, disoriented, and talking to people who aren't there.", label=TriageLabel.EMERGENCY),
        Scenario(id="mental_6", description="A 40-year-old reports losing interest in hobbies and feeling fatigued for the past month.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="mental_7", description="Acute panic attack: heart racing, sweating, and 'feeling of impending doom' for 5 minutes.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="mental_8", description="A person has ingested a large amount of unidentified pills in a suicide attempt.", label=TriageLabel.EMERGENCY),
        Scenario(id="mental_9", description="Chronic anxiety about health and checking symptoms online daily.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="mental_10", description="Sudden change in personality following a head injury, becoming aggressive and confused.", label=TriageLabel.EMERGENCY),

        # --- PEDIATRICS (10) ---
        Scenario(id="peds_1", description="A 3-year-old child has a temperature of 102°F (38.9°C) for the past 24 hours, is alert and drinking.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="peds_2", description="A 2-month-old infant is difficult to wake up and has not had a wet diaper in over 8 hours.", label=TriageLabel.EMERGENCY),
        Scenario(id="peds_3", description="A 4-year-old has a loud 'barking' cough and high-pitched stridor while at rest.", label=TriageLabel.EMERGENCY),
        Scenario(id="peds_4", description="A 5-year-old child has a red, itchy rash on their stomach. No fever or other symptoms.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="peds_5", description="A 6-month-old infant with a fever of 104F and a new rash that looks like purple spots (petechiae).", label=TriageLabel.EMERGENCY),
        Scenario(id="peds_6", description="A toddler swallowed a small coin and is currently playful and breathing normally.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="peds_7", description="A 7-year-old has been vomiting and has diarrhea, but is currently staying hydrated.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="peds_8", description="A 3-week-old neonate has a rectal temperature of 101.5F.", label=TriageLabel.EMERGENCY),
        Scenario(id="peds_9", description="A child fell and scraped their knee; it is bleeding slightly but clean.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="peds_10", description="Projectile vomiting and severe dehydration in a 1-month-old infant.", label=TriageLabel.EMERGENCY),

        # --- GASTROINTESTINAL (10) ---
        Scenario(id="gi_1", description="A 19-year-old has severe pain in the lower right abdomen that is worse when pressure is released.", label=TriageLabel.EMERGENCY),
        Scenario(id="gi_2", description="A 28-year-old has had three episodes of vomiting after eating at a new restaurant. No pain.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="gi_3", description="A 45-year-old is vomiting bright red blood.", label=TriageLabel.EMERGENCY),
        Scenario(id="gi_4", description="A 50-year-old reports black, tarry stools (melena) and feels very lightheaded.", label=TriageLabel.EMERGENCY),
        Scenario(id="gi_5", description="Mild heartburn after eating a large, spicy meal.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="gi_6", description="Pain in the upper right abdomen that started 1 hour after a fatty meal, radiating to the right shoulder.", label=TriageLabel.NON_EMERGENCY), # Cholecystitis (not always emergency)
        Scenario(id="gi_7", description="Severe, unrelenting abdominal pain that makes the person guard their stomach (rigid abdomen).", label=TriageLabel.EMERGENCY),
        Scenario(id="gi_8", description="A 30-year-old has mild constipation for 2 days; no pain or vomiting.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="gi_9", description="Sudden onset of massive, painless rectal bleeding.", label=TriageLabel.EMERGENCY),
        Scenario(id="gi_10", description="Chronic bloating and gas after eating dairy products.", label=TriageLabel.NON_EMERGENCY),

        # --- TRAUMA / SKIN (15) ---
        Scenario(id="trauma_1", description="I burned my finger on the stove. It's red and stings a bit, but no blisters.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="trauma_2", description="A person fell 10 feet from a ladder, hit their head, and was unconscious for 30 seconds.", label=TriageLabel.EMERGENCY),
        Scenario(id="trauma_3", description="A person has a deep cut on their forearm that is spurting blood and won't stop with pressure.", label=TriageLabel.EMERGENCY),
        Scenario(id="trauma_4", description="A 30-year-old sprained their ankle while jogging. It's swollen but they can bear weight on it.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="trauma_5", description="Severe eye pain and vision loss after being splashed with a chemical cleaner.", label=TriageLabel.EMERGENCY),
        Scenario(id="trauma_6", description="Full-thickness (third-degree) burns on the entire chest and arms.", label=TriageLabel.EMERGENCY),
        Scenario(id="trauma_7", description="A small splinter in the finger that is easily removable.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="trauma_8", description="A person was bitten by a stray dog on the hand, and the wound is deep.", label=TriageLabel.EMERGENCY),
        Scenario(id="trauma_9", description="A 15-year-old has a jammed finger from basketball; it's a bit bruised but they can move it.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="trauma_10", description="Obvious deformity and bone protruding through the skin after a car accident.", label=TriageLabel.EMERGENCY),
        Scenario(id="trauma_11", description="An itchy mosquito bite on the leg.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="trauma_12", description="Sudden onset of severe, painful swelling of the mouth after a bee sting.", label=TriageLabel.EMERGENCY),
        Scenario(id="trauma_13", description="Minor sunburn on the shoulders after a day at the beach.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="trauma_14", description="Penetrating wound from a nail in the foot, person has not had a tetanus shot in 20 years.", label=TriageLabel.NON_EMERGENCY), # Urgent but usually not 'ER now' unless symptomatic
        Scenario(id="trauma_15", description="Large, infected boil on the back that is warm and painful.", label=TriageLabel.NON_EMERGENCY),

        # --- MISC / SURGICAL / REPRO (15) ---
        Scenario(id="misc_1", description="User asks: 'Can I take ibuprofen with my blood pressure medication? I feel fine, just curious.'", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="misc_2", description="A 16-year-old reports sudden, severe pain in the right testicle that started 1 hour ago.", label=TriageLabel.EMERGENCY),
        Scenario(id="misc_3", description="A 50-year-old reports losing 15 pounds unexpectedly over the last 3 months.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="misc_4", description="Runner collapsed, skin hot and dry, confused on a 95F day.", label=TriageLabel.EMERGENCY),
        Scenario(id="misc_5", description="Severe flank pain (lower back) that is intermittent and 'worse than childbirth'.", label=TriageLabel.NON_EMERGENCY), # Kidney stones (painless but not life threatening usually)
        Scenario(id="misc_6", description="Sudden, painless swelling of the face and lips (angioedema).", label=TriageLabel.EMERGENCY),
        Scenario(id="misc_7", description="A woman who is 38 weeks pregnant has regular contractions every 3 minutes.", label=TriageLabel.NON_EMERGENCY), # Labor is expected
        Scenario(id="misc_8", description="A woman who is 30 weeks pregnant has sudden vaginal bleeding and sharp abdominal pain.", label=TriageLabel.EMERGENCY),
        Scenario(id="misc_9", description="Burning with urination (dysuria) and frequent trips to the bathroom.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="misc_10", description="A 60-year-old man cannot urinate and feels extremely uncomfortable in his lower abdomen.", label=TriageLabel.EMERGENCY), # Urinary retention
        Scenario(id="misc_11", description="A 25-year-old has had a low-grade fever and mild body aches for 2 days.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="misc_12", description="Excessive thirst, frequent urination, and blurred vision that has developed over weeks.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="misc_13", description="Diabetic patient is found sweaty, shaky, and now becoming difficult to arouse.", label=TriageLabel.EMERGENCY), # Hypoglycemia
        Scenario(id="misc_14", description="Small, painless lump found in the breast during self-exam.", label=TriageLabel.NON_EMERGENCY),
        Scenario(id="misc_15", description="Severe, stabbing ear pain that suddenly improved with some fluid drainage.", label=TriageLabel.NON_EMERGENCY),
    ]
