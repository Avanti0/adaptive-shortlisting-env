import scala.io.Source
import scala.util.Random

// Constants
val GREEN = 'G'
val AMBER = 'Y'
val BLACK = 'R'
val WIN = "GGGGG"

class WordleBot(name: String, seed: Option[Long] = None) {

  private val rand = seed match {
    case Some(s) => new Random(s)
    case None => new Random()
  }

  // Load all words from file once
  private val allWords: List[String] = try {
    val source = Source.fromFile("five_letter_words.txt")
    val lines = source.getLines().map(_.strip().toUpperCase).toList
    source.close()
    lines
  } catch {
    case _: java.io.FileNotFoundException =>
      println("Error: five_letter_words.txt not found.")
      sys.exit(1)
  }

  // Game state variables
  var secretWord: String = ""
  var words: List[String] = Nil
  var tries: Int = 0
  val allowed: Int = 6
  var status: String = "PLAY"
  var guess: String = ""
  var response: String = ""

  // Initialize first game
  reset()

  def reset(newSeed: Option[Long] = None): Unit = {
    newSeed.foreach(s => rand.setSeed(s))
    secretWord = allWords(rand.nextInt(allWords.length))
    words = allWords
    tries = 0
    status = "PLAY"
    guess = allWords(rand.nextInt(allWords.length))
    response = ""
  }

  def getFeedback(secret: String, guess: String): String = {
    val feedback = Array.fill(5)(BLACK)
    val secretChars = secret.toCharArray
    val guessChars = guess.toCharArray
    val usedSecret = Array.fill(5)(false)
    val usedGuess = Array.fill(5)(false)

    // First pass: Greens
    for (i <- 0 until 5) {
      if (guessChars(i) == secretChars(i)) {
        feedback(i) = GREEN
        usedSecret(i) = true
        usedGuess(i) = true
      }
    }

    // Second pass: Ambers
    for (i <- 0 until 5) {
      if (!usedGuess(i)) {
        var found = false
        for (j <- 0 until 5 if !found && !usedSecret(j)) {
          if (guessChars(i) == secretChars(j)) {
            feedback(i) = AMBER
            usedSecret(j) = true
            found = true
          }
        }
      }
    }

    feedback.mkString
  }

  def step(guessAttempt: String): Unit = {
    if (status != "PLAY") return

    tries += 1
    guess = guessAttempt.toUpperCase
    response = getFeedback(secretWord, guess)

    if (response == WIN) {
      status = "WON"
    } else if (tries >= allowed) {
      status = "EXCEEDED"
    } else {
      dropImpossibles()
      if (words.isEmpty) {
        status = "FAILED"
      }
    }
  }

  def dropImpossibles(): Unit = {
    words = words.filter(w => getFeedback(w, guess) == response)
  }

  def getNextGuess(): String = {
    if (words.isEmpty) return ""
    if (words.length == 1) return words.head

    val letterFrequencies = words.flatten.groupBy(identity).view.mapValues(_.size).toMap

    words.maxBy { word =>
      word.distinct.map(letterFrequencies.getOrElse(_, 0)).sum
    }
  }

  def play(): Unit = {
    val currentGuess = guess
    println(s"-- Attempt ${tries + 1} --")
    println(s"Guess    : $currentGuess")

    step(currentGuess)
    println(s"Feedback : $response")

    status match {
      case "WON" =>
        println("\nYay! The bot solved the Wordle!")
      case "EXCEEDED" =>
        println(s"Sorry, the bot could not guess the word. The answer was: $secretWord")
      case "FAILED" =>
        println("I have no more words to guess. Something went wrong.")
      case "PLAY" =>
        println(s"${words.length} possible words remaining.\n")
        guess = getNextGuess()
    }
  }

  def game(): Unit = {
    println(s"Starting local Wordle game for bot: $name")
    while (status == "PLAY") {
      play()
    }
  }
}

@main def runWordleBot(): Unit = {
  val bot = new WordleBot(name = "LocalScalaBot")
  bot.game()
}
