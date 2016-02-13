/**
    Copyright 2014-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

        http://aws.amazon.com/apache2.0/

    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
 */
package wiseguy;

import java.util.ArrayList;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.amazon.speech.slu.Intent;
import com.amazon.speech.speechlet.IntentRequest;
import com.amazon.speech.speechlet.LaunchRequest;
import com.amazon.speech.speechlet.Session;
import com.amazon.speech.speechlet.SessionEndedRequest;
import com.amazon.speech.speechlet.SessionStartedRequest;
import com.amazon.speech.speechlet.Speechlet;
import com.amazon.speech.speechlet.SpeechletException;
import com.amazon.speech.speechlet.SpeechletResponse;
import com.amazon.speech.ui.OutputSpeech;
import com.amazon.speech.ui.PlainTextOutputSpeech;
import com.amazon.speech.ui.SsmlOutputSpeech;
import com.amazon.speech.ui.Reprompt;
import com.amazon.speech.ui.SimpleCard;

/**
 * This sample shows how to create a Lambda function for handling Alexa Skill requests that:
 *
 * <ul>
 * <li><b>Session State</b>: Handles a multi-turn dialog model.</li>
 * <li><b>Custom slot type</b>: demonstrates using custom slot types to handle a finite set of known values</li>
 * <li><b>SSML</b>: Using SSML tags to control how Alexa renders the text-to-speech</li>
 * </ul>
 * <p>
 * <h2>Examples</h2>
 * <p>
 * <b>Dialog model</b>
 * <p>
 * User: "Alexa, ask Wise Guy to tell me a knock knock rap."
 * <p>
 * Alexa: "Knock knock"
 * <p>
 * User: "Who's there?"
 * <p>
 * Alexa: "<phrase>"
 * <p>
 * User: "<phrase> who"
 * <p>
 * Alexa: "<Punchline>"
 */
public class WiseGuySpeechlet implements Speechlet {

    private static final Logger log = LoggerFactory.getLogger(WiseGuySpeechlet.class);

    /**
     * Session attribute to store the stage the rap is at.
     */
    private static final String SESSION_STAGE = "stage";

    /**
     * Session attribute to store the current Rap ID.
     */
    private static final String SESSION_RAP_ID = "rapid";

    /**
     * Stage 1 indicates we've already said 'knock knock' and will set up the rap next.
     */
    private static final int RAP_STAGE = 1;
    /**
     * Stage 2 indicates we've set up the rap and will deliver the punchline next.
     */
    private static final int SETUP_STAGE = 2;

    /**
     * ArrayList containing knock knock raps.
     */
    private static final ArrayList<Rap> RAP_LIST = new ArrayList<Rap>();

    static {
        RAP_LIST.add(new Rap("I <break time=\"0.1s\" /> got <break time=\"0.5s\" /> a <break time=\"0.1s\" /> laptop in my back pocket <break time=\"0.1s\" /> My pen'll go off when I half-cock it Got a fat knot from that rap profit Made a living and a killing off it", "I got a laptop in my back pocket My pen'll go off when I half-cock it Got a fat knot from that rap profit Made a living and a killing off it", "I got a laptop in my back pocket My pen'll go off when I half-cock it Got a fat knot from that rap profit Made a living and a killing off it"));
    }

    @Override
    public void onSessionStarted(final SessionStartedRequest request, final Session session)
            throws SpeechletException {
        log.info("onSessionStarted requestId={}, sessionId={}", request.getRequestId(),
                session.getSessionId());

        // any initialization logic goes here
    }

    @Override
    public SpeechletResponse onLaunch(final LaunchRequest request, final Session session)
            throws SpeechletException {
        log.info("onLaunch requestId={}, sessionId={}", request.getRequestId(),
                session.getSessionId());

        return handleTellMeARapIntent(session);
    }

    @Override
    public SpeechletResponse onIntent(final IntentRequest request, final Session session)
            throws SpeechletException {
        log.info("onIntent requestId={}, sessionId={}", request.getRequestId(),
                session.getSessionId());

        Intent intent = request.getIntent();
        String intentName = (intent != null) ? intent.getName() : null;

        if ("LetsHaveARapBattle".equals(intentName)) {
            return handleTellMeARapIntent(session);
        } else if ("AfterRap".equals(intentName)) {
            return handleAfterRapIntent(session);
        } else if ("SetupNameWhoIntent".equals(intentName)) {
            return handleSetupNameWhoIntent(session);
        } else if ("AMAZON.HelpIntent".equals(intentName)) {
            String speechOutput = "";
            int stage = -1;
            if (session.getAttributes().containsKey(SESSION_STAGE)) {
                stage = (Integer) session.getAttribute(SESSION_STAGE);
            }
            switch (stage) {
                case 0:
                    speechOutput =
                            "Knock knock raps are a fun call and response type of rap. "
                                    + "To start the rap, just ask by saying tell me a"
                                    + " rap, or you can say exit.";
                    break;
                case 1:
                    speechOutput = "You can ask, who's there, or you can say exit.";
                    break;
                case 2:
                    speechOutput = "You can ask, who, or you can say exit.";
                    break;
                default:
                    speechOutput =
                            "Knock knock raps are a fun call and response type of rap. "
                                    + "To start the rap, just ask by saying tell me a "
                                    + "rap, or you can say exit.";
            }

            String repromptText = speechOutput;
            return newAskResponse(intentName, false, repromptText, false);
        } else if ("AMAZON.StopIntent".equals(intentName)) {
            PlainTextOutputSpeech outputSpeech = new PlainTextOutputSpeech();
            outputSpeech.setText("Goodbye");

            return SpeechletResponse.newTellResponse(outputSpeech);
        } else if ("AMAZON.CancelIntent".equals(intentName)) {
            PlainTextOutputSpeech outputSpeech = new PlainTextOutputSpeech();
            outputSpeech.setText("Goodbye");

            return SpeechletResponse.newTellResponse(outputSpeech);
        } else {
            throw new SpeechletException("Invalid Intent");
        }
    }

    @Override
    public void onSessionEnded(final SessionEndedRequest request, final Session session)
            throws SpeechletException {
        log.info("onSessionEnded requestId={}, sessionId={}", request.getRequestId(),
                session.getSessionId());

        // any session cleanup logic would go here
    }

    /**
     * Selects a rap randomly and starts it off by saying "Knock knock".
     *
     * @param session
     *            the session object
     * @return SpeechletResponse the speechlet response
     */
    private SpeechletResponse handleTellMeARapIntent(final Session session) {
        String speechOutput = "";

        // Reprompt speech will be triggered if the user doesn't respond.
        String repromptText = "Try your best to spit fire";

        // / Select a random rap and store it in the session variables
        int rapID = (int) Math.floor(Math.random() * RAP_LIST.size());

        // The stage variable tracks the phase of the dialogue.
        // When this function completes, it will be on stage 1.
        session.setAttribute(SESSION_STAGE, RAP_STAGE);
        session.setAttribute(SESSION_RAP_ID, rapID);
        speechOutput = "Alright mute spitter, let's see what you've got.";

        // Create the Simple card content.
        SimpleCard card = new SimpleCard();
        card.setTitle("Rap Battle");
        card.setContent(speechOutput);

        SpeechletResponse response = newAskResponse(speechOutput, false,
                repromptText, false);
        response.setCard(card);
        return response;
    }

    /**
     * Responds to the user saying "Who's there".
     *
     * @param session
     *            the session object
     * @return SpeechletResponse the speechlet response
     */
    private SpeechletResponse handleAfterRapIntent(final Session session) {
        String speechOutput = "", repromptText = "";
        if (session.getAttributes().containsKey(SESSION_STAGE)) {
            if ((Integer) session.getAttribute(SESSION_STAGE) == RAP_STAGE) {
                // Retrieve the rap's setup text.
                int rapID = (Integer) session.getAttribute(SESSION_RAP_ID);
                speechOutput = RAP_LIST.get(rapID).setup;

                // Advance the stage of the dialogue.
                session.setAttribute(SESSION_STAGE, SETUP_STAGE);

                repromptText = "You can ask, " + speechOutput + " who?";

            } else {
                session.setAttribute(SESSION_STAGE, RAP_STAGE);
                speechOutput = "That's not how knock knock raps work! <break time=\"0.3s\" /> Knock knock";
                repromptText = "You can ask who's there.";
            }
        } else {
            // If the session attributes are not found, the rap must restart.
            speechOutput =
                    "Sorry, I couldn't correctly retrieve the rap. You can say, tell me a rap.";
            repromptText = "You can say, tell me a rap.";
        }

        return newAskResponse("<speak>" + speechOutput + "</speak>", true, repromptText, false);
    }

    /**
     * Delivers the punchline of the rap after the user responds to the setup.
     *
     * @param session
     *            the session object
     * @return SpeechletResponse the speechlet response
     */
    private SpeechletResponse handleSetupNameWhoIntent(final Session session) {
        String speechOutput = "", repromptText = "";

        // Create the Simple card content.
        SimpleCard card = new SimpleCard();
        card.setTitle("Wise Guy");

        if (session.getAttributes().containsKey(SESSION_STAGE)) {
            if ((Integer) session.getAttribute(SESSION_STAGE) == SETUP_STAGE) {
                int rapID = (Integer) session.getAttribute(SESSION_RAP_ID);
                speechOutput = RAP_LIST.get(rapID).speechPunchline;
                card.setContent(RAP_LIST.get(rapID).cardPunchline);

                // Create the ssml text output
                SsmlOutputSpeech outputSpeech = new SsmlOutputSpeech();
                outputSpeech.setSsml("<speak>" + speechOutput + "</speak>");

                // If the rap completes successfully, this function will end the active session
                return SpeechletResponse.newTellResponse(outputSpeech, card);
            } else {
                session.setAttribute(SESSION_STAGE, RAP_STAGE);
                speechOutput = "That's not how knock knock raps work! <break time=\"0.3s\" /> Knock knock";
                repromptText = "You can ask who's there.";

                card.setContent("That's not how knock knock raps work! Knock knock");

                // Create the ssml text output
                SsmlOutputSpeech outputSpeech = new SsmlOutputSpeech();
                outputSpeech.setSsml("<speak>" + speechOutput + "</speak>");
                PlainTextOutputSpeech repromptOutputSpeech = new PlainTextOutputSpeech();
                repromptOutputSpeech.setText(repromptText);
                Reprompt repromptSpeech = new Reprompt();
                repromptSpeech.setOutputSpeech(repromptOutputSpeech);

                // If the rap has to be restarted, then keep the session alive
                return SpeechletResponse.newAskResponse(outputSpeech, repromptSpeech, card);
            }
        } else {
            speechOutput =
                    "Sorry, I couldn't correctly retrieve the rap. You can say, tell me a rap";
            repromptText = "You can say, tell me a rap";
            card.setContent(speechOutput);
            SpeechletResponse response = newAskResponse(speechOutput, false,
                    repromptText, false);
            response.setCard(card);
            return response;
        }
    }

    /**
     * Wrapper for creating the Ask response from the input strings.
     *
     * @param stringOutput
     *            the output to be spoken
     * @param isOutputSsml
     *            whether the output text is of type SSML
     * @param repromptText
     *            the reprompt for if the user doesn't reply or is misunderstood.
     * @param isRepromptSsml
     *            whether the reprompt text is of type SSML
     * @return SpeechletResponse the speechlet response
     */
    private SpeechletResponse newAskResponse(String stringOutput, boolean isOutputSsml,
            String repromptText, boolean isRepromptSsml) {
        OutputSpeech outputSpeech, repromptOutputSpeech;
        if (isOutputSsml) {
            outputSpeech = new SsmlOutputSpeech();
            ((SsmlOutputSpeech) outputSpeech).setSsml(stringOutput);
        } else {
            outputSpeech = new PlainTextOutputSpeech();
            ((PlainTextOutputSpeech) outputSpeech).setText(stringOutput);
        }

        if (isRepromptSsml) {
            repromptOutputSpeech = new SsmlOutputSpeech();
            ((SsmlOutputSpeech) repromptOutputSpeech).setSsml(repromptText);
        } else {
            repromptOutputSpeech = new PlainTextOutputSpeech();
            ((PlainTextOutputSpeech) repromptOutputSpeech).setText(repromptText);
        }
        Reprompt reprompt = new Reprompt();
        reprompt.setOutputSpeech(repromptOutputSpeech);
        return SpeechletResponse.newAskResponse(outputSpeech, reprompt);
    }

    private static class Rap {

        private final String setup;
        private final String speechPunchline;
        private final String cardPunchline;

        Rap(String setup, String speechPunchline, String cardPunchline) {
            this.setup = setup;
            this.speechPunchline = speechPunchline;
            this.cardPunchline = cardPunchline;
        }
    }
}
